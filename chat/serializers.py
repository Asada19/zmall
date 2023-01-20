from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# class MessageSerializer(serializers.Serializer):
#     message = serializers.CharField(max_length=200)
#
#     def create(self, validated_data):
#         data = {
#             "message": validated_data["message"],
#             "user": User.objects.get(pk=validated_data["user_id"])
#         }
#         message = Message.objects.create(**data)
#         return message