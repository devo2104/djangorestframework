from django.urls import path, include
from . import views, mixins
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', mixins.ProductMixinView.as_view(), name='product-list'),
    path('auth/', obtain_auth_token),
    path('create/', mixins.ProductMixinView.as_view(), name='product-create-view'),
    path('<int:pk>/', mixins.ProductMixinView.as_view(), name='product-alt-view'),
    path('detail/<int:pk>/', mixins.ProductMixinView.as_view(), name='product-detail-view'),
    path('update/<int:pk>/', mixins.ProductMixinView.as_view(), name='product-update-view'),
    path('delete/<int:pk>/', mixins.ProductMixinView.as_view(), name='product-delete-view'),

]
