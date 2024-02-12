# Generated by Django 5.0.1 on 2024-02-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('number', models.BigIntegerField(unique=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('dob', models.DateField(null=True)),
                ('gender', models.CharField(max_length=50, null=True)),
                ('date_joined', models.DateTimeField()),
                ('otp_field', models.CharField(max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
            ],
        ),
    ]
