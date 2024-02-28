from django.contrib import admin
from .models import Brand, Category
# Register your models here.

admin.site.register(Brand)
admin.site.unregister(Brand)
admin.site.register(Category)