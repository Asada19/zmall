from django.db import models
from django.utils.text import slugify
from transliterate import translit

from user.models import CustomUser


def get_upload_path_ad_image(instance, filename):
    return "ad_images/{username}/{file}".format(username=instance.advertisement.username(), file=filename)


def get_upload_path_head_image(instance, filename):
    return "ad_images/{username}/{file}".format(username=instance.username(), file=filename)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, blank=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, allow_unicode=True)
            self.slug = translit(slug, "ru", reversed=True)
        return super().save(*args, **kwargs)


class SubCategory(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, blank=True, db_index=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='sub_category')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, allow_unicode=True)
            self.slug = translit(slug, "ru", reversed=True)
        return super().save(*args, **kwargs)


class Advertisement(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    sub_category = models.ForeignKey(to=SubCategory, on_delete=models.DO_NOTHING, related_name='advertisements')
    price = models.PositiveIntegerField(default=0)
    max_price = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(blank=True, default=0)
    city = models.CharField(max_length=150, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def username(self):
        return self.owner.username

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title, allow_unicode=True)
            self.slug = translit(slug, "ru", reversed=True)
        return super().save(*args, **kwargs)


class PromoType(models.TextChoices):
    vip = "vip", "VIP"
    urgently = "urgently", "Срочно"
    highlighted = "highlighted", "Выделить"


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    types = models.CharField(max_length=50, choices=PromoType.choices, blank=True, null=True)
    price = models.FloatField()


class AdvertisementPromotion(models.Model):
    advertisement = models.ForeignKey(to=Advertisement, on_delete=models.PROTECT, related_name='promotions')
    promotion = models.ForeignKey(to=Promotion, on_delete=models.CASCADE, related_name='sub_promotion')


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to=get_upload_path_ad_image, blank=True, null=True)


class AdvertisementComment(models.Model):
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="sub_comment")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=5000)

    def __str__(self):
        return f"{self.advertisement} - comment"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class AdvertisementStatistic(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="statistic")
    created_on = models.DateTimeField(auto_now_add=True)
    ad_views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.advertisement.id}-{self.created_on}"

    class Meta:
        verbose_name = "статистика"
        verbose_name_plural = "статистика"


