from django.contrib.auth import get_user_model
from rest_framework import serializers
from advertisement.models import Advertisement, Category, SubCategory, AdvertisementImage, AdvertisementComment, \
    AdvertisementPromotion, Promotion
from django.utils import timezone

User = get_user_model()


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'price']


class AdvertisementPromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvertisementPromotion
        fields = ['id',  'advertisement']


class AdvertisementCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementComment
        fields = ['id', ]


class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image', 'advertisement']


class AdvertisementSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    comments = AdvertisementCommentSerializer(many=True, read_only=True)
    promotions = AdvertisementPromotionSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'slug', 'description', 'sub_category', 'price',
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'images', 'comments', 'promotions']


class SubCategorySerializer(serializers.ModelSerializer):
    advertisements = AdvertisementSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'title', 'slug', "advertisements")


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'sub_category')



