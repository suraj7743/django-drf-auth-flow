from rest_framework import serializers
from notifications.models import Notification
from django.contrib.auth import get_user_model


User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    connection_request = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'connection_request', 'message', 'created_at', 'is_read']
        read_only_fields = ['created_at', 'connection_request']