from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from advertisement.helpers import modify_input_for_multiple_files
from advertisement.permissions import IsOwnerOrReadOnly, IsCommentOwner
from core.db_management.debugger import query_debugger
from core.db_management.queries import get_ads_filtered, create_chat_room
from advertisement.models import Advertisement, Category, SubCategory, Promotion, \
    AdvertisementImage, Favorite, AdvertisementStatistic, AdvertisementComment
from advertisement.serializers import AdvertisementSerializer, CategorySerializer, SubCategorySerializer, \
    AdvertisementImageSerializer, FavoriteSerializer, AdvertisementDetailSerializer, \
    AdvertisementCommentSerializer, PromotionSerializer, StatisticSerializer
from django.contrib.auth.models import AnonymousUser


class AdvertisementListView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    filter_backends = (SearchFilter, )
    serializer_class = AdvertisementSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('title', 'description')

    @query_debugger
    def get_queryset(self):
        queryset = Advertisement.objects.filter(is_active=True).select_related('sub_category')
        price = self.request.query_params.get('price')
        max_price = self.request.query_params.get('max_price')
        city = self.request.query_params.get('city')
        has_image = self.request.query_params.get('has_image')

        if any([price, max_price, city, has_image]):
            queryset = get_ads_filtered(price=price, max_price=max_price, city=city, has_image=has_image)
        return queryset

    price = openapi.Parameter('price', openapi.IN_QUERY,
                              type=openapi.TYPE_NUMBER)
    max_price = openapi.Parameter('max_price', openapi.IN_QUERY,
                                  type=openapi.TYPE_NUMBER)
    city = openapi.Parameter('city', openapi.IN_QUERY,
                             type=openapi.TYPE_STRING)
    has_image = openapi.Parameter('has_image', openapi.IN_QUERY,
                                  type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[price, max_price, city, has_image])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        if self.request.user != AnonymousUser:
            create_chat_room(instance.id, self.request.user.id)


class OnModerationAPIView(ListAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Advertisement.objects.filter(is_active=False).select_related('sub_category')

    def get_queryset(self):
        return self.queryset.select_related('sub_category').filter(owner=self.request.user, is_active=False)


class AdvertisementImageAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        ads_id = request.data['advertisement']

        images = dict(request.data.lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(ads_id, img_name)
            file_serializer = AdvertisementImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class AdvertisementDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'
    queryset = Advertisement.objects.all()
    model = Advertisement
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertisementDetailSerializer


class CategoryListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = Category
    queryset = Category.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    parser_classes = (JSONParser, )
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SubCategoryListAPIView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = SubCategory
    queryset = SubCategory.objects.select_related('category').all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (SearchFilter, )
    serializer_class = SubCategorySerializer


class SubCategoryDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = SubCategory.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'


class AdvertisementPromotionListAPIView(ListAPIView):
    model = Promotion
    queryset = Promotion.objects.prefetch_related('advertisement').all()
    serializer_class = PromotionSerializer
    filter_backends = (SearchFilter, )


class AdvertisementFavoriteAPIView(ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteAPIView(DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=FavoriteSerializer,
                         operation_summary='Removes advertisement from favorites')
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        queryset = Favorite.objects.filter(user=user, advertisement__slug=request.data['advertisement'])
        if queryset.exists():
            queryset.delete()
            return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
        return Response('Advertisement does not exist in favorite', status=status.HTTP_404_NOT_FOUND)


class ShowStatisticView(APIView):
    def get(self, request, *args, **kwargs):
        statistics = AdvertisementStatistic.objects.filter(advertisement__id=kwargs['advertisement'])
        serializer = StatisticSerializer()


class CommentAPIView(CreateAPIView):
    serializer_class = AdvertisementCommentSerializer
    permission_classes = [IsAuthenticated, ]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdvertisementCommentSerializer
    permission_classes = (IsAuthenticated, IsCommentOwner)
    parser_classes = (MultiPartParser, FormParser)
    queryset = AdvertisementComment.objects.all()

