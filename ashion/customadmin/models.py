from django.db import models
from manage_product.models import products
from manage_category.models import Category


# Create your models here.


class Product_Offer(models.Model):
    product_id = models.ForeignKey(products, on_delete=models.SET_NULL, null=True)
    percentage = models.FloatField(null=True, blank=True, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)


class Category_Offer(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    percentage = models.FloatField(null=True, blank=True, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
