from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    '''
    http methods -> actual functions called -> what they do? 
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail view
    post -> create -> New Instance
    put -> update -> Update Instance
    patch -> update -> Partial Update Instance
    delete -> destroy -> Destroy model Instance
    '''
    queryset = Product.objects.all().order_by('title') 
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default
      

# So this is the heirarchy
    
    # function-based views
    # class-based views(they can implement the functions override too)
    # mixins(they implement the class-based views)
    # viewsets(they implement the mixins)



# if you want to be more flexible use GenericViewset and implement what you needed, as it will not provide 
    # anything by default

# to see all of the urls support by current viewset as turning them to actual variable and saying
    
class ProductGenericViewset(viewsets.GenericViewSet, 
                            mixins.ListModelMixin, 
                            mixins.CreateModelMixin, 
                            mixins.RetrieveModelMixin):
    
    queryset = Product.objects.all().order_by('title') 
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default

    @action(detail=True,methods=['patch', 'put'], url_name='UP')
    # if you don't mention any name for this function view, it will replace _ with -
    # so explicity mention url_name to namkaran this methods name to access via reverse()
    def update_product(self, request, pk=None):
        product = Product.objects.get(pk=pk) if pk else self.get_object()
        print(product, pk)
        # Since, this is all manual, i need to even pass the product object in order to update
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save(content=request.data.get('content'))
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

product_list_view = ProductGenericViewset.as_view({'get': 'list'})
product_detail_view = ProductGenericViewset.as_view({'get': 'retrieve'})

# Now i can use these variables as my view functions in the url patterns, easy 

