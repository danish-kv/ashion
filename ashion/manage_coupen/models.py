from django.db import models

# Create your models here.



class Coupons(models.Model):
    title = models.CharField(max_length = 50, null=True, blank=True)
    code = models.CharField(max_length = 50, unique = True, null=True, blank=True)
    discount_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveBigIntegerField(null=True, blank=True)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)