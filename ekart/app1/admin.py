from django.contrib import admin
from app1.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "cat", "product_details", "is_active", "p_img"]
    list_filter = [ "cat", "is_active"]


admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)