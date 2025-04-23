from rest_framework import serializers
from connections.models import ConnectionRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'company_name']

class ConnectionRequestSerializer(serializers.ModelSerializer):
    from_user = UserSearchSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
        read_only_fields = ['from_user', 'created_at']

class ReceivedConnectionRequestSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = ['id', 'sender', 'status']  # Include id, sender, status

    def get_sender(self, obj):
        return {
            'username': obj.from_user.username,
            'full_name': obj.from_user.full_name,
            'company_name': obj.from_user.company_name
        }