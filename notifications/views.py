from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]



    def get_queryset(self):
        # Only return notifications for the authenticated user
        return self.queryset.filter(recipient=self.request.user)
    
    def perform_create(self, serializer):
        # Ensure recipient is the authenticated user
        serializer.save(recipient=self.request.user)


    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})