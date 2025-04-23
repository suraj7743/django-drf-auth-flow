from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from rest_framework import status , permissions
from .models import ConnectionRequest
from django.db import IntegrityError

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .serializers import UserSearchSerializer, ConnectionRequestSerializer, ReceivedConnectionRequestSerializer

User = get_user_model()


# Create your views here.

class SearchUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q','')
        users= User.objects.filter(
            models.Q(full_name__icontains=query) |
            models.Q(company_name__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(contact_number__icontains=query)
        ).exclude(id=request.user.id)

        return Response(UserSearchSerializer(users, many=True).data)
    

class SendConnectionRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        print("Request data:", data)
        data['from_user'] = request.user.id

        # Validate to_user ID
        try:
            to_user_id = data.get('to_user')
            if not to_user_id:
                return Response({"error": "to_user ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            to_user = User.objects.get(id=to_user_id)
            if to_user == request.user:
                return Response({"error": "You cannot send a connection request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        except (ObjectDoesNotExist, ValueError):
            return Response({"error": "Invalid to_user ID"}, status=status.HTTP_400_BAD_REQUEST)

        print("Modified data:", data)

        serializer = ConnectionRequestSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save(from_user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "Connection request already exists for this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class RespondToConnectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        print("Request data:", request.data)
        try:
            connection = ConnectionRequest.objects.get(id=pk, to_user=request.user)
        except ConnectionRequest.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status_val = request.data.get('status')
        print("Status value:", status_val)
        if status_val in [ConnectionRequest.ACCEPTED, ConnectionRequest.REJECTED]:
            connection.status = status_val
            connection.save()

            from notifications.tasks import send_connection_notification
            send_connection_notification.delay(connection.id)
            return Response({'status': 'updated'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)   



class ListReceivedConnectionRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        received_requests = ConnectionRequest.objects.filter(to_user=request.user)
        serializer = ReceivedConnectionRequestSerializer(received_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)