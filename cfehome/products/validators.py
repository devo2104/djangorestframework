from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product


def validate_title(value):
        print('Ye aayi value yaha -----', value)
        queryset = Product.objects.filter(title__iexact=value)
        if queryset.exists():
            raise serializers.ValidationError(f'{value} is already present as product name')
        
        return value