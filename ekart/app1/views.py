from django.shortcuts import render,HttpResponse, redirect
from app1.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from app1.models import *
from django.db.models import Q
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import default_storage
from .send_msg import *
from django.db import transaction
from twilio.rest import Client



# Create your views here.
def register(request):
    context={}
    if request.method == "POST":
        uname=request.POST['uname']
        upassword=request.POST["upassword"]
        ucpassword=request.POST["cpassword"]
        if uname=="" or upassword=="" or ucpassword =='':
            context['errmsg']='Field can not be empty'
            return render(request,'register.html',context)
        elif upassword !=ucpassword:
            context['errmsg']='password and cpassword didnt match'
            return render(request,'register.html',context)    
        else:
            try:
                u=User.objects.create_user(username=uname,password=upassword)
                u.save()
                return HttpResponse("Success!!")
            except Exception:
                context['errmsg']='Username already exist'
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
            

def about(request):
    return render(request,"about.html")

def  userlogin(request):
    context = {}
    if request.method == "POST":
        nm = request.POST["uname"]
        pw = request.POST["upassword"]
        if nm == "" or pw == "":
            context['errmsg']="Fields cannot be Empty"
            return render(request, "login.html", context)
        else:
            u = authenticate(username=nm, password=pw)
            if u is not None:
                login(request,u)
                return redirect("/allproducts/")
            else:
                context["errmsg"]= "Invalid Username and password"
                return render(request,"login.html",context)
        
    else:
        return render(request, "login.html")


def user_logout(request):
    print(request.user)
    logout(request)
    return redirect('/login/')


def all_product(request):
    product = Product.objects.filter(is_active = True)
    context = {}
    context["Products"] = product
    print(product)
    return render(request, "home.html", context)

def catfilter(request,cf):
    context = {}
    q1 = Q(cat=cf)
    q2 = Q(is_active = True)
    product = Product.objects.filter(q1 & q2)
    print(product)
    context["Products"] = product
    return render(request,'home.html',context)



def sortbyprice(request, sv):
    if sv == '1':
        products = Product.objects.filter(is_active=True).order_by("-price")
    else:
        products = Product.objects.filter(is_active=True).order_by("price")
    
    context = {'Products': products}
    return render(request, "home.html", context)


def filterbyprice(request):
    mn = request.GET["min"]
    mx= request.GET["max"]
    q1 = Q(price__gte=mn)
    q2 = Q(price__lte=mx)
    q3 = Q(is_active=True)
    product = Product.objects.filter(q1 &q2 &q3)
    context = {}
    context["Products"] = product
    print(mn,mx)
    return render(request,'home.html',context)

def username(request):
    user = request.user
    return render(request, 'home.html', {'user': user})

def search(request):
    query = request.GET['query']
    p = Product.objects.filter(name__icontains = query)
    context = {"Products": p, "query": query}
    return render(request, "home.html",context)
    # return HttpResponse("Working!!")  

def search2(request):
    query2 = request.GET['query2']
    user_id = request.user
    c = Cart.objects.filter(user_id = user_id, pid__name__icontains = query2)
    context = {'cart_items':c , "query":query2 }
    return render(request,"cart.html",context)

def productDetails(request,pid):
    context = {}
    prod = Product.objects.filter(id = pid)
    context["Product"] = prod
    return render (request, 'product_details.html', context)

def cart(request, pid):
    if request.user.is_authenticated:
        uid = request.user
        product = Product.objects.get(id = pid)
        if Cart.objects.filter(user_id = uid, pid = product).exists():
            prod = Product.objects.filter(id = pid)           
            already_message = "Product Already exist in Cart!! "
            context = {"already" : already_message, "Product": prod}
            return render(request, "product_details.html", context)
        else:
            c = Cart.objects.create(user_id = uid, pid = product)
            prod = Product.objects.filter(id = pid)
            context = {"success": "Product Added Successfully!!", "Product": prod}
            return render(request, "product_details.html", context)

def cartdetails(request):
    cart_items = Cart.objects.filter(user_id=request.user.id)
    order_details = None
    product = []
    qty = []
    total_price = 0
    get_product_price = 0

    
    
    for item in cart_items:
            total_price += item.pid.price * item.qty
            product.append(item.pid.name)
            qty.append(item.qty)

    if total_price < 1.0:
        return render (request, "empty_cart.html")

    try:
        order_details = DeliveryDetails.objects.get(user=request.user)
    except DeliveryDetails.DoesNotExist:
        pass

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': total_price * 100 ,  "currency": 'INR', "payment_capture" : 1})
    razor_pay_order_id = payment['id']

    for cart_item in cart_items:
        cart_item.razor_pay_order_id = payment['id']
        create_order(razor_pay_order_id, request.user, cart_item)
        cart_item.save()


    print("**********")
    print(payment)
    print("**********")

    context = {
        'cart_items': cart_items,
        'order_details': order_details,
        "total": total_price,
        "n": len(cart_items),
        "products_with_qty": zip(product, qty),
        "get_product_price": get_product_price,
        "payment": payment,
    }


    return render(request, 'cart.html', context)

def create_order(order_id, user, cart_item):
   Order.objects.create(razor_pay_order_id=order_id, user_id=user, cid=cart_item, qty=cart_item.qty)


account_sid = 'ACbfed8c1c91885dd1d48676eefeb41fa2'
auth_token = 'd5a830829dae4f195475e38c30ce699d'
client = Client(account_sid, auth_token)

def success(request):
    order_id = request.GET.get('order_id')
    product_details_qty = [] 
    total = []
    final = 0
    name = []
    try:
        delivery_details = DeliveryDetails.objects.get(user=request.user)
        orders = Order.objects.filter(razor_pay_order_id=order_id)

        for order in orders:
            order.payment_successful = True
            order.is_active = False
            order.save()
            carts = Cart.objects.filter(order=order)
            for cart in carts:
                total_price = cart.pid.price * cart.qty
                product_details_qty.append((cart.pid, cart.qty, total_price))
                final += total_price
                name.append(cart.pid.name)
        Cart.objects.filter(order__razor_pay_order_id=order_id).delete()
        html_message = render_to_string('email_template.html', {'order': order, 'product_details_qty': product_details_qty, 'total': total, 'final': final})
        plain_message = strip_tags(html_message)
        send_mail(
            'Payment Successful',
            plain_message,
            'thakurkaustubh37@gmail.com',
            [delivery_details.email],
            html_message=html_message,
            fail_silently=False,
        )
        message_body = 'Order placed Successfully, Check mail for more details,\n Product names are: {}\n😊'.format(', '.join(name))
        print(message_body)
        message = client.messages.create(
        from_='+12567279802',
        body=message_body,
        to='+919156748282')
        return render(request, "payment_done.html")
    except ObjectDoesNotExist:
        return HttpResponse("Order not found")
    


def navbar(request):
    return render(request, "navbar.html")

def delete(request, rid):
    product = Cart.objects.filter(id = rid)
    product.delete()
    return redirect('/cartdetails')

def updateqty(request,x,cid):
    c = Cart.objects.filter( id = cid)
    q = c[0].qty
    print(c)
    if x == '1':
        q = q + 1
    elif q > 1:
        q = q - 1
    c.update(qty = q)
    return redirect('/cartdetails')

def placeorder(request):
    return render (request,'placeorder.html')

def orderdetails(request):
    if request.user.is_authenticated:
        try:
             delivery_details = DeliveryDetails.objects.get(user=request.user)
             return render(request, "demo.html", {'delivery_details': delivery_details})
        except  DeliveryDetails.DoesNotExist:
            if request.method == "POST":
                name = request.POST['uname']
                email = request.POST['uemail']
                address = request.POST['uaddress']
                state = request.POST["ustate"]
                city = request.POST["ucity"]
                zp = request.POST["uzipcode"]
                phone = request.POST["uphone"]
                user = User.objects.get(username= name)
                c = DeliveryDetails.objects.create(user = user, email = email, address = address, city = city, zip_code = zp, mobile_no = phone, state = state )
                c.save()
                return redirect ('/cartdetails')
            else :
                return render(request, "order_details.html")
            
def editdetails(request, rid):
    if request.method == "GET":
        c = DeliveryDetails.objects.filter(id = rid)
        context = {}
        context ["deliverydetail"] = c 
        return render(request, "edit.html", context)
    else:
        name = request.POST['uname']
        email = request.POST['uemail']
        address = request.POST['uaddress']
        state = request.POST["ustate"]
        city = request.POST["ucity"]
        zp = request.POST["uzipcode"]
        phone = request.POST["uphone"]
        user = User.objects.get(username= name)
        c = DeliveryDetails.objects.filter(id = rid)
        c.update(user = user, email = email, address = address, city = city, zip_code = zp, mobile_no = phone, state = state)
        return redirect('/cartdetails')

def demo(request):
    return render (request, "demo.html")

def deletedetails(request, rid):
    c = DeliveryDetails.objects.filter(id = rid)
    c.delete()
    return redirect("/cartdetails")



