# Generated by Django 5.0.2 on 2024-02-13 07:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manage_product", "0012_alter_products_gender_variant"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="variant",
            unique_together={("product_id", "size", "color")},
        ),
    ]