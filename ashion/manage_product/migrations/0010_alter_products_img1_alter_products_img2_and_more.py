# Generated by Django 5.0.1 on 2024-02-10 04:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manage_product", "0009_alter_products_brand"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="img1",
            field=models.ImageField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="products",
            name="img2",
            field=models.ImageField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="products",
            name="img3",
            field=models.ImageField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="products",
            name="img4",
            field=models.ImageField(upload_to="images/"),
        ),
    ]
