# Generated by Django 5.0.2 on 2024-03-07 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "customadmin",
            "0002_category_offer_end_date_category_offer_start_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="category_offer",
            name="percentage",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product_offer",
            name="percentage",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]