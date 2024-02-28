from django.db import models
from logintohome.models import Customer
from manage_product.models import products

# Create your models here.



class Wishlist(models.Model):
    user_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product_id = models.ForeignKey(products, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user_id}'s Wishlist"
     