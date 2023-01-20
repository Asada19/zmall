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

    def test_user_creation(self):
        data = {
            'email': 'sample2@gmail.com',
            'first_name': 'second',
            'last_name': 'last',
            'password': 'strongpass12345'
        }

        start = time.time()
        response = self.client.post(reverse('api-register'), data, format='json', content_type='application/json')
        end = time.time()

        self.assertLess(end - start, 0.3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['user']['is_active'])

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo', first_name='Ad',
                                                   last_name='Min')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
