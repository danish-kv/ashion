# Generated by Django 5.0.2 on 2024-02-26 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
        ("manage_product", "0016_remove_products_stock_remove_variant_color_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wishlist",
            name="product_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="manage_product.products",
            ),
        ),
    ]