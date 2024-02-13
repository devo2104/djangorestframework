from rest_framework.routers import DefaultRouter 
from products.viewsets import ProductViewSet, ProductGenericViewset


router = DefaultRouter()
router.register('product-abc', ProductGenericViewset, basename='products')

# print(router.urls) # This will automatically gets print when you run the server, as it will load all the files for us and do the neccessary running of the files, create objects, sessions, migrations etc..

# # Products List
#     URLPattern('^product-abc/$', [name='products-list']),
#     URLPattern('^product-abc\.(?P<format>[a-z0-9]+)/?$', [name='products-list']),

#     # Product Detail
#     URLPattern('^product-abc/(?P<pk>[^/.]+)/$', [name='products-detail']),
#     URLPattern('^product-abc/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$', [name='products-detail']),

#     # API Root
#     URLPattern('^$', [name='api-root']),

#     # API Root with Format
#     URLPattern('^\.(?P<format>[a-z0-9]+)/?$', [name='api-root']),


urlpatterns = router.urls