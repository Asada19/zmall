from django.contrib.auth import get_user_model
from rest_framework import serializers
from advertisement.models import Advertisement, Category, SubCategory, AdvertisementImage, AdvertisementComment, \
    AdvertisementPromotion, Promotion, Favorite, AdvertisementStatistic
from django.utils import timezone

User = get_user_model()


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'price']


class AdvertisementPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementPromotion
        fields = ['id', 'advertisement', 'promotion']


class PromotionDestroySerializer(serializers.ModelSerializer):
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
        fields = ['id', 'image', 'advertisement']


class AdvertisementSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    promotion = AdvertisementPromotionSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'slug', 'description', 'sub_category', 'price',
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'images', 'comments', 'promotions']


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    comments = AdvertisementCommentSerializer(many=True, read_only=True)
    promotion = AdvertisementPromotionSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'sub_category', 'price',
                  'max_price', 'views', 'city', 'end_date', 'created_on', 'images', 'comments', 'promotion']


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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'advertisement', 'created_at')


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementStatistic
        fields = '__all__'
