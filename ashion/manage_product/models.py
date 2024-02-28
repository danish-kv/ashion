from django.db import models
from manage_category.models import Category

# Create your models here.




class products(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    priority = models.IntegerField(default= 1)
    img1 = models.ImageField(upload_to="media/")
    img2 = models.ImageField(upload_to="media/")
    img3 = models.ImageField(upload_to="media/")
    img4 = models.ImageField(upload_to="media/")
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    SIZE_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]

    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, null = True, blank=True)
    stock = models.PositiveIntegerField(default=0, null=True, blank=True)

    # color = models.CharField(max_length=20, null=True, blank=True, default = 'white')

    def __str__(self):
        return f"{self.product_id.name} - {self.size}"
    
    
