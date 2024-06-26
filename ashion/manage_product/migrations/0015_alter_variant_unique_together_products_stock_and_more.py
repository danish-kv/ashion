# Generated by Django 5.0.2 on 2024-02-13 14:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manage_product", "0014_remove_products_brand_remove_products_gender"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="variant",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="products",
            name="stock",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.RemoveField(
            model_name="variant",
            name="stock",
        ),
    ]
