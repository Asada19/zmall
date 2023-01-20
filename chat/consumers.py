import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from advertisement.models import Advertisement
from chat.utils import write_message_to_db

User = get_user_model()


@database_sync_to_async
def get_owner(id):
    try:
        return Advertisement.objects.get(id=int(id)).owner.id
    except ObjectDoesNotExist:
        return None


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if self.scope["user"] is AnonymousUser:
            await self.close()

        self.ad_id = self.scope['url_route']['kwargs']['ad_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = f"{self.ad_id}-{self.user_id}"


        ad_owner = await get_owner(self.ad_id)
        if not ad_owner:
            await self.close()

        if self.scope["user"].id != int(self.user_id) and self.scope["user"].id != ad_owner:
            await self.close()

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        await write_message_to_db(self.ad_id, self.user_id, text_data)
        await self.channel_layer.group_send(
            self.room_name,
            {"type": "chat_message",
             "text": text_data,
             "sender": f'{self.scope["user"].first_name} {self.scope["user"].last_name}'}
        )

    async def chat_message(self, event):
        message = event["text"]
        sender = event["sender"]

        await self.send(text_data=f"{sender}: {message}")

    async def disconnect(self, code):
        pass
