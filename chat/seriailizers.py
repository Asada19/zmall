from rest_framework import serializers
from django.contrib.auth import get_user_model

from advertisement.models import Advertisement
from chat.utils import create_chat_room

User = get_user_model()

class ChatRoomSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        cr = create_chat_room(validated_data['ad_id'], validated_data['user_id'])
        return cr