# Generated by Django 5.0.2 on 2024-02-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manage_order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderedproducts",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "Order Confirmed"),
                    (2, "Order Processed"),
                    (3, "Order Delivered"),
                    (4, "Order Rejected"),
                ]
            ),
        ),
    ]
