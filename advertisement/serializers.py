from django.contrib.auth import get_user_model
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import serializers
from rest_framework.response import Response

from advertisement.models import Advertisement, Category, SubCategory, AdvertisementImage, AdvertisementComment, \
    Promotion, Favorite, AdvertisementStatistic, AdvertisementPromotion
from django.utils import timezone

User = get_user_model()


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'price', 'types']


class AdsPromoSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer(many=True, read_only=True)

    class Meta:
        model = AdvertisementPromotion
        fields = ['id', 'promotion']


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class AdvertisementCommentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)
    parent_id = serializers.IntegerField(required=False)
    user = serializers.StringRelatedField(read_only=True)

    def validate(self, parent):
        if parent == 0:
            return None
        return parent

    class Meta:
        model = AdvertisementComment
        fields = ('id', 'user', 'advertisement', 'body', 'parent_id', 'children')


class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image']


class AdvertisementSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    promotions = AdsPromoSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'slug', 'description', 'sub_category', 'price',
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'upload_images',
                  'images', 'promotions']

        extra_kwargs = {
            "upload_images": {
                "required": False,
            },
        }

    def create(self, validated_data):
        upload_images = validated_data.pop('upload_images', None)
        advertisement = Advertisement.objects.create(**validated_data)
        if upload_images:
            for image in upload_images:
                AdvertisementImage.objects.create(advertisement=advertisement, image=image)
        return advertisement


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    comments = AdvertisementCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'sub_category', 'price',
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'images', 'comments']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'title', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'sub_category')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'advertisement', 'created_at')


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementStatistic
        fields = '__all__'
