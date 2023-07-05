from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/<str:room_name>/',consumers.ChatConsumer.as_asgi()),
    path('personal/ws/<int:id>/',consumers.Personalchatconsumer.as_asgi())
    
]