# Generated by Django 5.0.2 on 2024-04-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_order_payment_successful'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
        migrations.AddField(
            model_name='cart',
            name='razor_pay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]