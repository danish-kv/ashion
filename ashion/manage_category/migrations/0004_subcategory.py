# Generated by Django 5.0.1 on 2024-02-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manage_category", "0003_remove_category_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subcategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
    ]
