from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins, permissions, authentication


# Create your views here.


# I have used GET request in Postman
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer  
    lookup_field = 'id'  # i have to mention this same keyword in the url too

    # if you want your custom queryset then

    # def get_queryset(self):
    #     return super().get_queryset()
    
    # To use post method you have to explicitly mention this method 

    # def post(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     print(instance)
    #     print(serializer)
    #     if serializer.is_valid(raise_exception=True):
    #         return Response(serializer.data)


# I have used POST request
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    

    # you can use custom perform_create to create a model instance 

    def perform_create(self, serializer):
        # All this function do, is save the serializer and believe me it will save the data in model.
        # if you want to pass extra fields that are not in the serializer fields, you can do here in save()
        serializer.save(user=self.request.user, content=self.request.data.get('content'))


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        print(self.request.user)
        qs = super().get_queryset(*args, **kwargs) 

        if not self.request.user.is_authenticated:
            return Product.objects.none()

        return qs.filter(user=self.request.user)
    

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method 

    if method == 'GET':  
        if pk is not None:
            # detail-view
            obj = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(obj)
            return Response(serializer.data)
        else:
            # list-view
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
            
    elif method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): 
            title = serializer.validated_data.get('title')
            print(title)
            instance = serializer.save(content=request.data['content'])
            print(instance) 
            return Response(serializer.data)
        


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'



    def perform_update(self, serializer):
        print(serializer.is_valid())
        # the object here is the database record for the lookup field pk=1 (self.get_object())
        # any update is done on the object of the Model class.
        # like you can only change the attributes of the class that's it.
        instance = serializer.save()


# There can be error with url, so check that too..

class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'



    def perform_destroy(self, instance):
        # give this funtion the model instance you want to delete
        print(instance)
        super().perform_destroy(instance)


        


     
     
# Fact - Before doing anything with permissions we have to do authentication my dear! 

# With the DjangoModelPermission, even when you remove the can view products form the django admin settings.
# You can't view the Model in the admin page, but when you visit the api page, you can actually look all the products , so to handle that you can create your custom DjangoModel for that
    

