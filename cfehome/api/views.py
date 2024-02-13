import json
from .models import Product
from .serializers import ProductSerializer
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


# Create your views here.
def api_home(request):
    # request -> Httprequest instance hai from django
    body = request.body 
    # we need to convert it to python dict data using json.loads
    
    print(body) # This is the byte string of json data or json string

    data = {}
    try:
        data = json.loads(body) # deserialize the data to dictionary from json
    except:
        pass
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type

    query_params = request.GET # to fetch all the query variables in the url
    print(query_params) # <QueryDict: {'abc': ['123']}>
    print(query_params.get('abc')) # 123
    
    data['params'] = dict(request.GET)

    print(data.keys(), '\n', data) # this means the data here is python dict
    return JsonResponse(data)


def api_model_view(request, *args, **kwargs):
    model_data = Product.objects.all().order_by('?').first() # this is the reference object instance
    data = {}
    print(args, kwargs)
    if model_data:
        data['id'] = model_data.id
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price

    print(data)
    # the most verbose way of doing it
        # model instance
        # turn a python dict
        # turn into json object - serialize the data
        # we are performing serialization here.
        # returning the json object to client
    # there is another way of doing it using django.forms.model 

    # HttpResponse default return type is text/html but you can explicity mention the type to return json.

    # to get the json string from python dict use json.dumps(dict)

    Data = model_to_dict(model_data, fields=['id', 'title', 'price'])
    print(type(Data))
    return JsonResponse(data)


# Now we will work with api_view class for the functions

@api_view(['GET', 'POST'])
def api_rest_view(request, *args, **kwargs):
    # to get query params you can do it 2 ways
    Q1 = request.GET
    Q2 = request.query_params
    print(Q1 == Q2) # Truef
    instance = Product.objects.all()
    serializer = {}  
    # model instance -> json object
    # serialization,  so no need to pass data argument with .is_valid bhi available nahi hoga
    # you can have multiple serailizer for the same model
    if instance:
        serializer = ProductSerializer(instance, many=True)
    # The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
    # Original exception text was: 'QuerySet' object has no attribute 'title'.
    # You will get this error if you don't mention many=True for multiple instances from queryset
    print(serializer, end='\n')
    print(type(serializer))
    return Response(serializer.data)



# Taking json data from client and then using Serialization for validation is Deserialization

# if json pass it with data=request.data or else if model instance pass it directly to serialize 

@api_view(['POST'])
def api_view_rest_save(request, *args, **kwargs):
    print(request.query_params)
    print(request.data)
    # it will validate my json data injected from client
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True): # this will notify client side with more robust error details
        instance = serializer.save() # it will save all the fields in model class, those not mention fields will be None
        print(instance.content)
        print(serializer.data) # it will show only those fields that are mention in fields in class Meta serializer
        return JsonResponse(serializer.data)

# if you try to use serializerFields without creating and saving the model instance using .save() command, 
# it will throw error for serializerMethodFields as the obj.get_discount() , obj was never created
# obj - Product model instance
    
# if you are not saving the serializer, then the all fields which are not part of serializer will not get
    # added to response, but if they are null=True or blank=True, they will get added, with explicitly mentioned fields

# validate requirements of serializer first, then the model class requirements too of json data (de-serlization)
    
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer  
    lookup_field = 'id'  # i have to mention this same keyword in the url too

    # if you want your custom queryset then

    # def get_queryset(self):
    #     return super().get_queryset()
    
    # To use post method you have to explicitly mention this method 

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        print(instance)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)

  
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
