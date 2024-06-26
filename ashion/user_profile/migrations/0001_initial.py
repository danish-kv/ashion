# Generated by Django 5.0.2 on 2024-02-12 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("logintohome", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("name", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("district", models.CharField(max_length=100)),
                ("landmark", models.CharField(blank=True, max_length=100, null=True)),
                ("address", models.TextField()),
                ("number", models.BigIntegerField()),
                ("alternate_number", models.BigIntegerField(blank=True, null=True)),
                ("pincode", models.BigIntegerField()),
                ("is_available", models.BooleanField(default=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="logintohome.customer",
                    ),
                ),
            ],
        ),
    ]
