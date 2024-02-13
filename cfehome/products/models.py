from django.db import models
from django.conf import settings
from django.db.models import Q
import math

User = settings.AUTH_USER_MODEL # auth.User


class ProductQuerySet(models.QuerySet):

    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs2 | qs).distinct()
        return qs


class ProductManager(models.Manager):
    # It already inherits the Queryset class, which is like storing all the db operations ..

    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        return ProductQuerySet(self.model, self._db)

 
    def search(self, query, user=None):
        print('---------------------- search')
        return self.get_queryset().search(query, user=user)

# Create your models here.
class Product(models.Model):
    #pk
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True) 
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99) 
    public = models.BooleanField(default=True)


 
    objects = ProductManager()

    @property
    def sales_price(self):
        return "%.2f" %(float(self.price) * 0.8)
    

    def get_discount(self):
        n = self.price
        pw =  1 if n == 0 else int(math.log10(abs(n))) + 1
        div = math.pow(10, pw)
        print(div)
        print((float(self.price) / div) * 100 * 0.5) 
        return "%.0f" %((float(self.price) / div) * 100 * 0.47) + "% Off! Hurry"