from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import transaction
from notifications.models import Notification
from connections.models import ConnectionRequest

User = get_user_model()

@shared_task
def send_connection_notification(connection_id):
    print(f"Processing task for ConnectionRequest ID: {connection_id}")
    try:
        with transaction.atomic():
            connection = ConnectionRequest.objects.get(id=connection_id)
            print(f"Found ConnectionRequest: from_user={connection.from_user.id}, to_user={connection.to_user.id}, status={connection.status}")
            message = f"Your connection request to {connection.to_user.username} was {connection.get_status_display().lower()}."
            notification = Notification.objects.create(
                recipient=connection.from_user,
                connection_request=connection,
                message=message
            )
            print(f"Created Notification ID: {notification.id}")
            return f"Notification created for ConnectionRequest {connection_id}"
    except ConnectionRequest.DoesNotExist:
        print(f"ConnectionRequest with ID {connection_id} does not exist")
        raise  # Re-raise to log the error in Celery
    except Exception as e:
        print(f"Error creating notification for ConnectionRequest {connection_id}: {str(e)}")
        raise  # Re-raise to log the error in Celery