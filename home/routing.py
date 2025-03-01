from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/socket-server/<str:room_code>/', consumers.VideoEvent.as_asgi())
]