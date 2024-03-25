from django.db import models
from manage_category.models import Category
from decimal import Decimal
# Create your models here.


class products(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)
    img1 = models.ImageField(upload_to="media/")
    img2 = models.ImageField(upload_to="media/")
    img3 = models.ImageField(upload_to="media/")
    img4 = models.ImageField(upload_to="media/")
    is_listed = models.BooleanField(default=True)

    def discounted_price(self):
        pro_offer = self.product_offer_set.first()
        cat_offer = self.category.category_offer_set.first()

        if pro_offer and cat_offer:
            if pro_offer.is_active == True and cat_offer.is_active == True:
                pro_discount = self.selling_price * (
                    Decimal(pro_offer.percentage) / 100
                )
                cat_discount = self.selling_price * (
                    Decimal(cat_offer.percentage) / 100
                )
                offer = min(pro_discount, cat_discount)
                return int(self.selling_price - offer)

            elif pro_offer.is_active == True and cat_offer.is_active == False:
                offer = self.selling_price * (Decimal(pro_offer.percentage) / 100)
                return int(self.selling_price - offer)

            elif pro_offer.is_active == False and cat_offer.is_active == True:
                offer = self.selling_price * (Decimal(cat_offer.percentage) / 100)
                return int(self.selling_price - offer)

            else:
                return int(self.selling_price)

        elif pro_offer and pro_offer.is_active == True:
            offer = self.selling_price * (Decimal(pro_offer.percentage) / 100)
            return int(self.selling_price - offer)

        elif cat_offer and cat_offer.is_active == True:
            offer = self.selling_price * (Decimal(cat_offer.percentage) / 100)
            return int(self.selling_price - offer)

        else:
            return int(self.selling_price)

    def __str__(self):
        return self.name


class Variant(models.Model):
    SIZE_CHOICES = [("S", "Small"), ("M", "Medium"), ("L", "Large")]

    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product_id.name} - {self.size}"
