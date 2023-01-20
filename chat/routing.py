from django.urls import re_path

from chat import consumers


websocket_urlpatterns = [
    re_path(r'message/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
