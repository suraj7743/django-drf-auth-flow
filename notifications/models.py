from django.db import models
from django.contrib.auth import get_user_model
from connections.models import ConnectionRequest
# Create your models here.

User = get_user_model()



class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    connection_request = models.ForeignKey(ConnectionRequest, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"