# Generated by Django 5.0.2 on 2024-03-07 09:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0006_wallet_user_balance"),
    ]

    operations = [
        migrations.AddField(
            model_name="wallet_user",
            name="transaction_type",
            field=models.CharField(default="Credit", max_length=50),
            preserve_default=False,
        ),
    ]