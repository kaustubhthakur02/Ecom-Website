from django.contrib import admin
from django.urls import path, include
from app1 import views
from django.conf.urls.static import static
from django.conf import settings
from app1 import urls


urlpatterns = [
    path('',views.all_product, name= 'allproducts' ),
    path('register/', views.register, name="register"),
    path('login/', views.userlogin, name='login'),
    path('about/', views.about, name='about'),
    path('logout/', views.user_logout, name='logout'),
    path('details/', views.all_product, name='product'),
    path('catfilter/<cf>/', views.catfilter),
    path('sortbyprice/<sv>/', views.sortbyprice),
    path('allproducts/', views.all_product, name= 'allproducts'),
    path('filterbyprice/', views.filterbyprice),
    path('search/',views.search, name= "search"),
    path("product_details/<pid>/", views.productDetails, name="productdetails"),
    path('addcart/<pid>/', views.cart),
    path('cartdetails/', views.cartdetails, name="cartdetails"),
    path('navbar/', views.navbar, name= "navbar"),
    path('remove/<rid>/',views.delete),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('placeorder/', views.placeorder, name= "placeorder"),
    path('search2/',views.search2 ,name= 'search2'),
    path('orderdetails/', views.orderdetails, name = "orderdetails"),
    path('edit/<rid>', views.editdetails, name= "edit"),
    path('demo/', views.demo, name="demo"),
    path('delete2/<rid>', views.deletedetails),
    path('cartdetails/success/', views.success, name="success"),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)