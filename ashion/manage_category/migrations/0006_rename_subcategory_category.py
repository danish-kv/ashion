# Generated by Django 5.0.1 on 2024-02-08 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_category', '0005_rename_category_brand'),
        ('manage_product', '0006_rename_orginal_price_products_original_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subcategory',
            new_name='Category',
        ),
    ]
