from django.db import models
from logintohome.models import Customer

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.BigIntegerField()
    address = models.TextField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank = True, null = True)
    pincode = models.BigIntegerField()
    alternate_number = models.BigIntegerField(blank = True,null = True)
    is_available = models.BooleanField(default=True, null=True)

    def __str__(self) -> str:
        return f"'{self.name}'s address "