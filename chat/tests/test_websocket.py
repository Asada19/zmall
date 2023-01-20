from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from time import time

User = get_user_model()



from channels.testing import WebsocketCommunicator

from config.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


class WebsocketTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email="user@example.com",
            first_name="User",
            last_name="User",
            is_active=True
        )

    @staticmethod
    def get_object(obj=User, pk=1):
        return obj.objects.get(pk=pk)

    def setUp(self):
        user = self.get_object(obj=User, pk=1)
        self.client.force_authenticate(user)


    async def test_can_connect_to_server(self):
        communicator = WebsocketCommunicator(
            application=application,
            path='/msg/'
        )
        connected, _ = await self.communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()
