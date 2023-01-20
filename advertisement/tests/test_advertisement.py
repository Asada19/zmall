from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from time import time

from advertisement.models import Advertisement, Category, SubCategory

User = get_user_model()


class AdvertisementTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email="user@example.com",
            first_name="User",
            last_name="User",
            is_active=True
        )
        user.set_password("cantrem21")
        cat = Category.objects.create(
            title="Cat"
        )
        subcategory = SubCategory.objects.create(
            title="SubCat",
            category=cat
        )
        Advertisement.objects.create(
            title="New Ad",
            owner=user,
            description="Lorem Ipsum",
            sub_category=subcategory,
            price=12_000,
            city="Bishkek",
            end_date=timezone.now()
        )

    @staticmethod
    def get_object(obj=Advertisement, pk=1):
        return obj.objects.get(pk=pk)

    def setUp(self):
        user = self.get_object(obj=User, pk=1)
        self.client.force_authenticate(user)

    def test_advertisements_get(self):
        start = time()
        response = self.client.get(reverse("advertisement-list"), format='json')
        end = time()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertLess(end-start, 0.25)

    def test_advertisements_post(self):
        subcategory = self.get_object(obj=SubCategory)

        data = {
            "title": "New Ad2",
            "description": "Lorem Ipsum2",
            "sub_category": subcategory.id,
            "city": "Bishkek",
        }

        start = time()
        response = self.client.post(reverse("advertisement-list"), data)
        end = time()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertLess(end-start, 0.009)

    def test_advertisements_get_by_pk(self):
        ad = self.get_object()

        start = time()
        response = self.client.get(reverse("advertisement-detail", kwargs={"slug": ad.slug}), format='json')
        end = time()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertLess(end - start, 0.25)
