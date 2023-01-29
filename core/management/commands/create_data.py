import random
from django.core.management.base import BaseCommand
from advertisement.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        Advertisement.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()

        categories = [Category(title=f"Category{index}", slug=f'category{index}{index}') for index in range(1, 6)]
        Category.objects.bulk_create(categories)

        for category in Category.objects.all():
            sub_categories = [SubCategory(title=f"Sub-category{index}{index}",
                                          slug=f'sub_category{random.randint(1, 9999)}',
                                          category=category)
                              for index in range(1, 6)]
            SubCategory.objects.bulk_create(sub_categories)

        counter = 0
        ads = []
        for sub in SubCategory.objects.all():
            for i in range(20):
                counter = counter + 1
                ads.append(Advertisement(title=f'Ads{counter}',
                                         slug=f'Ads{counter}{random.randint(1, 9999)}',
                                         owner_id=1,
                                         description='hello',
                                         sub_category=sub,
                                         price=random.randint(10, 555)))

        Advertisement.objects.bulk_create(ads)
