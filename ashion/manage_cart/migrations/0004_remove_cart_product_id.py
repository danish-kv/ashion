# Generated by Django 5.0.2 on 2024-02-16 16:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manage_cart", "0003_remove_cart_delete_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="product_id",
        ),
    ]