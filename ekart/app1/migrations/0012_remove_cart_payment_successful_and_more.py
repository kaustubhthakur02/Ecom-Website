# Generated by Django 5.0.2 on 2024-04-09 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_remove_order_payment_successful_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='payment_successful',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='razor_pay_order_id',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_successful',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_order_id',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
