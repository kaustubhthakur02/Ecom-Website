# Generated by Django 5.0.2 on 2024-04-13 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_order_processed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='processed',
        ),
    ]
