from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    # This points to project level
    # My biggest mistake is creating a folder for the django project, never do that
    # when you run command django-admin startproject projectName,
    # this is enough, it will create a new project with all the requirements you ever needed to start with
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('products/', include('products.urls')), 
    path('api/v2/', include('cfehome.routers')),
    path('api/search/', include('search.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
]
