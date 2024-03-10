from django.db import models
from logintohome.models import Customer
from manage_product.models import *
from manage_coupen.models import Coupons
# Create your models here.

class Cart(models.Model):
    user_id = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
    size_variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"'{self.user_id}'s cart"




class Checkout(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons, on_delete=models.SET_NULL, null=True)
    coupon_active = models.BooleanField(default=False, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)



    