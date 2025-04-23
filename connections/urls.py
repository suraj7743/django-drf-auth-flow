from django.urls import path
from .views import SearchUserView, SendConnectionRequestView, RespondToConnectionView, ListReceivedConnectionRequestsView


app_name = 'connections'  
urlpatterns=[
    path('search/', SearchUserView.as_view(), name='user-search'),
    path('connect/', SendConnectionRequestView.as_view(), name='send-connection'),
    path('respond/<int:pk>/', RespondToConnectionView.as_view(), name='respond-connection'),
    path('received/', ListReceivedConnectionRequestsView.as_view(), name='list-received-connections'),
]