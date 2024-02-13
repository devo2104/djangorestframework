from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # my_discount = serializers.SerializerMethodField(read_only=True)
    # we can also include the normal methods of Model class and the properties too in the serializers
    # also we can give them differnt names too, other than defined in Model class
    class Meta:
        model = Product 
        fields = ['title', 'price', 'sales_price'] 
    

    def get_my_discount(self, obj):
        # obj is here the instance of api.models.Product class, jis model ka ye serializer hai basically
        print(obj, type(obj))
        try:
            return obj.get_discount();
        except:
            return None