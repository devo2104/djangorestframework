from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title


# querysets and model instances, into native Python datatypes - work of serialization
# encapsulate it in Response builtin function, it will convert it into json data

# deserialization, ek format set kardeta hai, wahi milna chayiye frontend json raw data se

# you can even source the 'user.product_set.all' which is the queryset i guess

# Custom managers allow you to encapsulate complex or frequently used query logic in one place, promoting code organization and reusability.

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='products-detail', lookup_field='pk', read_only=True)
    
    title = serializers.CharField(read_only=True)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField() # you don't need to mention read_only=True, if they exits by default
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    other_products = serializers.SerializerMethodField(read_only=True)


    def get_other_products(self, obj):
        print(obj)
        user = obj
        my_products_qs = user.product_set.all()[:5] # foreign key relationships
        # if now i serialize the product using ProductSerializer, it will recursion exceed as circular import will occur, a deadlock
        # so i will create a new Serializer for it.

        print(my_products_qs)

        request = self.context.get('request')

        return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data
        return UserProductInlineSerializer(my_products_qs, many=True, context={'request': request}).data


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source='user') # saare fields hamesha UserSerializer ke andar define crow
    email = serializers.EmailField(source='user.email')
    # if the field is not present but you know the source, then also you don't have to mention read_only
    title = serializers.CharField(validators=[validate_title])
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='products-detail', lookup_field='pk')
    my_user_data = serializers.SerializerMethodField(read_only=True)
    # we can also include the normal methods of Model class and the properties too in the serializers
    # also we can give them differnt names too, other than defined in Model class
    class Meta:
        model = Product 
        # By default, all the model fields on the class will be mapped to a corresponding serializer fields.
        fields = ['owner', 'email', 'pk', 'url', 'edit_url', 'title', 'price', 'sales_price', 'my_discount', 'my_user_data', 'public']# these are fields that will show in json response and get saved in database
        # if you don't mention some fields here and even you pass it in json client, it will not save in database
        # exclude = ['content']

    def get_my_discount(self, obj):
        # obj is here the instance of api.models.Product class, jis model ka ye serializer hai basically
        print(obj, type(obj))
        try:
            return obj.get_discount()
        except:
            return None


    def get_edit_url(self, obj):
        # return f'/api/v2/products/{obj.pk}'    
        request = self.context.get('request') # self.request, but when you do manual then you required to do this
        print(request)
        if request is None:
            return None
        return reverse('products-UP', kwargs={'pk': obj.pk}, request=request)    
    

    def get_my_user_data(self, obj):
        return {
            'username': obj.user.username
        }

    
    # def validate_title(self, value):
    #     print('Ye aayi value yaha -----', value)
    #     queryset = Product.objects.filter(title__iexact=value)
    #     if queryset.exists():
    #         raise serializers.ValidationError(f'{value} is already present as product name')
        
    #     return value
    


# Keep in mind that the serializer.data attribute is only available after calling the is_valid() method on the serializer instance if you’re deserializing data. However, when serializing data, you can directly access the serializer.data attribute after instantiating the serializer class with the data to be serialized.

# saving something in model is actually - Deserialization
# Now when deserializing data, we can call .save() to return an object instance, based on the validated data.
        
#  the full_name field in the serializer is associated with the name attribute in the model using the source argument. This means that when you serialize data, it will use the full_name field, and when you deserialize data, it will update the name attribute in the model
        
# you don't have to write the fields that are already in the model in the serializer , just to include them
    # in the fields array

# view will definitely have the request attribute, but the serializer may or not, you can explicity pass
    # the request fields as context in the serializer instance 


