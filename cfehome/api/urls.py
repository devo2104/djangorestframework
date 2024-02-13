from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.api_home, name='api_home'),
    path('model/', views.api_model_view, name='api_model_view'),
    path('rest/', views.api_rest_view, name = 'api_rest_view'),
    path('save/', views.api_view_rest_save, name='api_view_rest_save'),
    path('retrieve/<int:id>/', views.ProductDetailView.as_view(), name='product_detail_view'),
    path('create/', views.ProductCreateAPIView.as_view(), name='product_create_view'),
    
]