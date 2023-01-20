from django.urls import path
from . import views
from .views_api import *

urlpatterns = [
    path('create/', views.create_ad_view, name='create_adv'),
    # api
    path('advertisement/', AdvertisementListView.as_view(), name='advertisement-list'),
    path('advertisement/<slug:slug>', AdvertisementDetailAPIView.as_view(), name='advertisement-detail'),
    path('advertisement/add-image', AdvertisementImageAPIView.as_view(), name='add-image'),
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<slug:slug>', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('sub-category/', SubCategoryListAPIView.as_view(), name='sub-category-list'),
    path('sub-category/<slug:slug>', SubCategoryDetailAPIView.as_view(), name='sub-category-detail'),
    path('promotion/', PromotionListAPIView.as_view(), name='promotion-list'),
    path('promotion/<int:pk>', PromotionDetailAPIView.as_view(), name='promotion-detail'),
    path('sub-promotion/', AdvertisementPromotionListAPIView.as_view(), name='sub-promotion-list'),
    path('sub-promotion/<int:pk>', AdvertisementPromotionDetailAPIView.as_view(), name='sub-promotion-detail'),
]