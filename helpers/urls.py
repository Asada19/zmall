from django.urls import path

from helpers.views import QuestionCategoryListAPIView, CallbackCreateAPIView, PolicyConfAPIView

urlpatterns = [
    path('help', QuestionCategoryListAPIView.as_view(), name='help'),
    path('call_back', CallbackCreateAPIView.as_view(), name='call_back'),
    path('policy_conf', PolicyConfAPIView.as_view(), name='policy_conf'),
]