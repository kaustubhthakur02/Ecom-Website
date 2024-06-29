from django.db import models
from  django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Create your models here.
class Product(models.Model):
    CAT = ((1,"SHOES"),(2,"Jacket"),(3, "Jeans"))
    name = models.CharField(max_length=50, verbose_name = "Product Name")
    price = models.IntegerField()
    cat = models.IntegerField( verbose_name = "Category", choices = CAT)
    product_details = models.CharField(max_length = 500, verbose_name ="Product Details")
    is_active = models.BooleanField(default=True, verbose_name = "Available")
    p_img = models.ImageField(upload_to= 'images',null= True )

    def __str__(self):
        return self.name

class Cart(models.Model):
    user_id=models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column="userid")
    pid=models.ForeignKey("Product", on_delete=models.CASCADE, db_column="pid")
    qty = models.IntegerField(default = 1)

    def get_product_price(self):
        return self.pid.price * self.qty

class Order(models.Model):
    razor_pay_order_id = models.CharField(max_length = 100, default=None)
    user_id=models.ForeignKey('auth.User', on_delete=models.CASCADE,db_column="userid")
    cid = models.ForeignKey('Cart', on_delete=models.CASCADE,db_column="cartid")
    qty = models.IntegerField(default = 1)
    payment_successful = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name = "Available")


class DeliveryDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length = 20)

    def __str__(self):
        return f"name is{self.user}, address is{self.address}"
    
