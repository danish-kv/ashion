from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=200)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


class Category(models.Model):
    name = models.CharField(max_length=200)
    is_listed = models.BooleanField(default=True)
    def __str__(self):
        return self.name



    # CATEGORY_CHOICE = [('Shirt', 'shirt'), ('Pant', 'pant'), ('T-Shirt', 't-shirt'),
    #             ('Churidar', 'churidar'), ('Salwar', 'salwar'), ('Sarees', 'sarees'),('Skirts', 'skirts'),
    #             ('Frock',' frock'), ('Kids-Tshirt', 'kids-tshirt'), ('Kids-Pant', 'kids-pant'),
    #             ]