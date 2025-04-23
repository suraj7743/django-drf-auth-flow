from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer= UserSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User registered successfully ", status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    permission_classes= [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer= UserSerializer(user)
        return Response(serializer.data)