from django.urls import re_path

from chat import consumers


websocket_urlpatterns = [
    re_path(r'message/(?P<ad_id>[^/]+)/(?P<user_id>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
