import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status

User = get_user_model()


class UserTest(TestCase):

    @staticmethod
    def get_object(obj=User):
        return obj.objects.first()

    def setUp(self):
        user = User.objects.create(
            email="sample@gmail.com",
            first_name="User",
            last_name="User",
            is_active=True
        )
        user.set_password("strongpass123")
        user.save()

    def test_get_token(self):

        data = {
            'email': 'sample@gmail.com',
            'password': 'strongpass123'
        }

        start = time.time()
        response = self.client.post(reverse('api-token-obtain'), data, format='json', content_type='application/json')
        end = time.time()

        self.assertLess(end - start, 0.3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_object().is_active, True)

    def test_get_token_invalid_credentials(self):

        data = {
            'email': 'nonexistent@gmail.com',
            'password': 'nonex123'
        }

        start = time.time()
        response = self.client.post(reverse('api-token-obtain'), data, format='json', content_type='application/json')
        end = time.time()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertLess(start - end, 0.03)

    def test_activate_account_invalid_credentials(self):
        user = self.get_object()
        user.is_active = False
        user.save()

        key = f'{user.pk}-{user.is_active}'

        start = time.time()
        response = self.client.post(reverse('api-confirm-email', kwargs={'key': key}),
                                    format='json', content_type='application/json')
        end = time.time()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user.is_active, False)
        self.assertLess(start - end, 0.03)

    def test_activate_account(self):
        user = self.get_object()

        key = f'{user.pk}-{default_token_generator.make_token(user)}'

        start = time.time()
        response = self.client.post(reverse('api-confirm-email', kwargs={'key': key}),
                                    format='json', content_type='application/json')
        end = time.time()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.is_active, True)
        self.assertLess(start - end, 0.03)
