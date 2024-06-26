# Generated by Django 5.0.2 on 2024-03-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manage_coupen", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coupons",
            old_name="limit",
            new_name="quantity",
        ),
        migrations.AddField(
            model_name="coupons",
            name="min_amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
