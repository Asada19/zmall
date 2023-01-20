from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from time import time

from api_auth.tokens import RefreshToken, AccessToken

User = get_user_model()



from channels.testing import WebsocketCommunicator

from config.routing import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


class WebsocketTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="user@example.com",
            first_name="User",
            last_name="User",
            is_active=True
        )
        User.objects.create(
            email="user2@example.com",
            first_name="User2",
            last_name="User2",
            is_active=True
        )

    @staticmethod
    def get_object(obj=User, pk=1):
        return obj.objects.get(pk=pk)

    def setUp(self):
        refresh = RefreshToken

        self.access_token_us1 = refresh.create(1).access_token.token
        self.access_token_us2 = refresh.create(2).access_token.token
        self.chat_room = '1/2'
        self.complete_path = 'message/{}/?token={}'.format(self.chat_room, self.access_token_us1)
        self.communicator = WebsocketCommunicator(
            application=application,
            path=self.complete_path
        )

    async def test_can_connect_to_server(self):
        connected, _ = await self.communicator.connect()
        self.assertTrue(connected)

        await self.communicator.disconnect()

    async def test_can_connect_to_server_not_authenticated(self):
        connected, _ = await self.communicator.connect()
        self.assertFalse(connected)

        await self.communicator.disconnect()

    async def test_send_message(self):
        connected, _ = await self.communicator.connect()
        self.assertTrue(connected)

        message = {'type': 'chat_message', 'text': 'Hello, WebSocket!'}
        await self.communicator.send_json_to(message)

        response = await self.communicator.receive_json_from()
        self.assertEqual(response, message)

        await self.communicator.disconnect()

        self.client.assertIsNone(await self.communicator.receive_json_from())
