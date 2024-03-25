# Generated by Django 5.0.2 on 2024-03-06 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_alter_wishlist_product_id"),
        ("manage_product", "0018_rename_active_variant_is_listed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wishlist",
            name="product_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="manage_product.variant",
            ),
        ),
    ]