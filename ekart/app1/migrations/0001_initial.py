# Generated by Django 5.0.1 on 2024-03-06 07:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Product Name')),
                ('price', models.IntegerField()),
                ('cat', models.IntegerField(choices=[(1, 'SHOES'), (2, 'Jacket'), (3, 'Jeans')], verbose_name='Category')),
                ('product_details', models.CharField(max_length=500, verbose_name='Product Details')),
                ('is_active', models.BooleanField(default=True, verbose_name='Available')),
                ('p_img', models.ImageField(null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
            ],
        ),
    ]
