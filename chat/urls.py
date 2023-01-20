from django.urls import path, re_path
from chat import views

urlpatterns = [
    re_path(r'message/', views.MessageSendAPIView.as_view(), name='message'),
]
