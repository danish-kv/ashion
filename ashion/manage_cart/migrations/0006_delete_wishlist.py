# Generated by Django 5.0.2 on 2024-02-26 12:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manage_cart", "0005_checkout"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Wishlist",
        ),
    ]
