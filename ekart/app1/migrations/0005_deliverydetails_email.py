# Generated by Django 5.0.2 on 2024-03-09 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_deliverydetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverydetails',
            name='email',
            field=models.EmailField(default=0, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
