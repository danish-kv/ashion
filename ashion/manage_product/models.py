from django.db import models
from manage_category.models import Brand, Category

# Create your models here.

# ('Casual', 'casual'), ('Formal', 'formal'), ('Street-Style', 'street-style'),


class products(models.Model):

    GENDER = [('Men', 'men'), ('Women', 'women'), ('Kids', 'kids')]


    name = models.CharField(max_length=200)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField( max_length=10 , choices = GENDER, default='all')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null = True)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    priority = models.IntegerField(default= 1)
    img1 = models.ImageField(upload_to="media/")
    img2 = models.ImageField(upload_to="media/")
    img3 = models.ImageField(upload_to="media/")
    img4 = models.ImageField(upload_to="media/")
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name
