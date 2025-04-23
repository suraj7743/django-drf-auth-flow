from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notifications.views import NotificationViewSet
app_name = 'notifications'

router = DefaultRouter()
router.register('', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]