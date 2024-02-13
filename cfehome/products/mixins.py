from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics, mixins, permissions, authentication
from .permissions import IsStaffEditorPermission
from .authentication import TokenAuthentication


# After working with mixins with quite a time, i now realized why i needed it
# i needed it because let's say we want some functionality across multiple urlpattersn/views.
# it's a clown way to mention that feature in every view, why don't just create a class(mixins)
# for that functionality and just inherit that shit for every view that required/need it.


class UserQuerySetMixin():
    user_field = 'user'

    def get_queryset(self, *args, **kwargs):
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user
        qs = super().get_queryset()
        # Oh my god , **lookup_data was not working but below line worked lol
        # https://stackoverflow.com/questions/52612286/input-is-an-invalid-keyword-argument-for-print
        print(*lookup_data.values())
        # Because print doesn't have those keyword arguments, but will accept any number of positional arguments
        if self.request.user.is_staff:
            # when i put this, i am now able to view other members products those who are not superuser(i am superuser)
            return qs
        return qs.filter(**lookup_data)

# These are basically the classes, to do the crud operations and auth, perms, basically any functionality
class ProductMixinView(UserQuerySetMixin, mixins.ListModelMixin, 
                       mixins.RetrieveModelMixin, 
                       mixins.CreateModelMixin, 
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # if you will try to acesss(do any post request) this will throw and auth cred not provided
    # Because your postman has not logged in, and session data is only maintained for logged in users.
    # They are called Anonymous users!!
    # You have to serve the file  on the same url where the django server is hosted :clown:
    # But if really want frontend to pass the authentication, use TokenAuthentication for that
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsStaffEditorPermission]  
    # ordering of classes matters too..
     
    lookup_field = 'pk'

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset()
    #     if not self.request.user.is_authenticated:
    #         return Product.objects.none()
        
    #     return qs.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
             return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

    # If you don't mention these http methods explicity, it will say method not allowed, so implement it.

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)   

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 

    def perform_create(self, serializer):
        print('Proof it is getting overwrite')
        # now while creating the products, you don't have to explicitly mention the user field
        # whoever is logged in the django admin, uske product model instance create honge
        # but how do my postman knows that, good questions
        # it knows about it because i have provided auth details (Token for that username)
        # jisse bhi vo token associate hoga uska object banega
        serializer.save(user=self.request.user, content=self.request.data.get('content'))

    def perform_update(self, serializer):
        print('Proof it is getting overwrite')
        serializer.save(content=self.request.data.get('content'))


    def perform_destroy(self, instance):
        print('Proof it is getting overwrite')
        return super().perform_destroy(instance)
    

# instead of hardcoding permission classes in every view, just create a mixins and inherit it whichever class required it
