from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer



class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        query = self.request.query_params.get('q')
        # print('ye rahi query', query)
        results = Product.objects.none()
        if query is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
                # print('ye raha dekho user', user)
            results = queryset.search(query, user=user)
        print('Results------', results)
        return results