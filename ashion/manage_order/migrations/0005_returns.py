# Generated by Django 5.0.2 on 2024-02-21 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logintohome", "0001_initial"),
        ("manage_order", "0004_alter_orderedproducts_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Returns",
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
                ("reason", models.TextField(blank=True, null=True)),
                ("request_date", models.DateField(auto_now_add=True, null=True)),
                ("pickup_date", models.DateField(blank=True, null=True)),
                (
                    "order_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="manage_order.orderedproducts",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="logintohome.customer",
                    ),
                ),
            ],
        ),
    ]
