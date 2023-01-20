import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from advertisement.models import Advertisement
# from chat.utils import write_chatroom_to_db, write_message_to_db

User = get_user_model()


@database_sync_to_async
def get_advertisement(ad_id):
    try:
        return Advertisement.objects.get(id=int(ad_id))
    except:
        return None


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if self.scope["user"] is AnonymousUser:
            await self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.ad_id, self.user_id = self.room_name.split("-")
        advertisement = await get_advertisement(self.ad_id)
        if self.scope["user"].id != int(self.user_id) and self.scope["user"].id != int(advertisement.owner.id):
            await self.close()

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        # await write_chatroom_to_db({"advertisement": advertisement.id,
        #                             "customer": self.user_id})

        await self.accept()

    async def receive(self, text_data):
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
