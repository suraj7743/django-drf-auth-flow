from django.db import models
from django.conf import settings

# Create your models here.

class ConnectionRequest(models.Model):
    PENDING= 'P'
    ACCEPTED= 'A'
    REJECTED='R'
    STATUS_CHOICES=[(PENDING, 'Pending'),
                    (ACCEPTED, 'Accepted'), 
                    (REJECTED, 'Rejected')]
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('from_user', 'to_user')


