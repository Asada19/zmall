from django.urls import path
from . import views
from .views_api import *

urlpatterns = [
    path('create/', views.create_ad_view, name='create_adv'),
    # api
    path('advertisement/', AdvertisementListView.as_view(), name='advertisement-list'),
    path('advertisement/<int:pk>', AdvertisementDetailAPIView.as_view(), name='advertisement-detail'),
    path('advertisement/add-image', AdvertisementImageAPIView.as_view(), name='add-image'),
    path('advertisement/add_promotion/', AdvertisementPromotionDetailAPIView.as_view(), name='sub-promotion-detail'),
    path('advertisement/delete_promotion/', AdvertisementPromotionDestroyAPIView.as_view(), name='sub-promotion-detail'),
    path('on_moderate', OnModerationAPIView.as_view(), name='on_moderate'),
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<slug:slug>', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('sub-category/', SubCategoryListAPIView.as_view(), name='sub-category-list'),
    path('sub-category/<slug:slug>', SubCategoryDetailAPIView.as_view(), name='sub-category-detail'),
    path('favorites/', AdvertisementFavoriteAPIView.as_view(), name='favorite_list_create'),
    path('favorite_delete/', FavoriteDeleteAPIView.as_view(), name='favorite_delete')
]
