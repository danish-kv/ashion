from django.contrib import admin

from .models import products, Variant

# Register your models here.

admin.site.register(products)
admin.site.register(Variant)
