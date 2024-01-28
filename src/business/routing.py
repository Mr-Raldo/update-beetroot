from django.urls import re_path, path
from .consumers import BusinessSocketConsumer
from chat.consumers import ChatConsumer

business_websocket_patterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    path(r'ws/eprofile/<str:user_id>/', BusinessSocketConsumer.as_asgi())
]