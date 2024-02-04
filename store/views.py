from django.shortcuts import render, redirect
from .models import Product, Category, Customer, Orders
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
# Create your views here.

class Cart_page(View):
    def get(self, request):
        # result = request.session.get('cart') # hmko id nikalni hai product ki
        # Get selected product id
        product_id_list = list(request.session.get('cart').keys())
        # get product details using product id list:
        product_details = Product.objects.filter(id__in = product_id_list)
        return render(request, 'cart.html', {'products':product_details})

class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in = list(cart.keys()))
        # print(f"add : {address}\nphone : {phone}\n customer : {customer}\ncart : {cart}\nProduct : {products}")
        for product in products:
            order = Orders(
                customer = Customer(id=customer),
                product = product,
                price = product.price,
                address = address,
                phone = phone,
                quantity = cart.get(str(product.id))
            )
            order.save()
        request.session['cart'] = {}        
        return redirect('cart')

class Order_page(View):
    # @method_decorator(auth_middleware)
    def get(self, request):
        customer_id = request.session.get('customer')
        orders = Orders.objects.filter(customer = customer_id)
        orders = orders.order_by('-date')
        return render(request, 'orders.html',{'orders':orders})
    
class Index_page(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')

        print(f"Product id are == {product_id}")
        cart = request.session.get('cart')
        if cart:
            print(f"cart already value : {cart}")
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product_id)
                    else:    
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1    
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        print(f"Cart in console : {request.session['cart']}")
        return redirect('index')

    def get(self, request):
        print(f"Request method ===== {request.method}")
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_category()
        category_id = request.GET.get('category')
        print(f"category id = {category_id}")
        if category_id:
            products = Product.get_all_products_by_category_id(category_id)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print(f"Email id customer : {request.session.get('email')}")
        print(f"Data are == {data}")
        return render(request, 'index.html',data)

def user_logout(request):
    request.session.clear()
    return redirect('login')

class login_user(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        response = request.POST
        email = response.get('email')
        password = response.get('password')
        customer = Customer.get_customer_by_email(email)
        print(f"customer email is : {customer}")
        error_msg = ''
        if customer:
            flag = check_password(password, customer.password)
            print(f"Flag password are == {flag}")
            if flag:
                # create session ---
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                print(f"Current session are : {request.session}")
                return redirect('index')
            else:
                error_msg = "Password invalid !!"
        else:
            error_msg = "Email or Password invalid !!"
        return render(request, 'login.html', {'error':error_msg})

class user_signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        response = request.POST
        print(f"Response  = {response}")
        fname = response.get('fname')
        lname = response.get('lname')
        phone = response.get('phone')
        email = response.get('email')
        password = response.get('password') 

        #validation:
        value = {
            "fname":fname,
            "lname":lname, 
            "phone":phone,
            "email":email
        }
        error_msg = ""

        if not fname:
            error_msg = "First name is required !!"
        elif len(fname) < 4:
            error_msg = "First name must be 4 char or more"
        elif not lname:
            error_msg = "Last name is required !!"
        elif len(lname) < 3:
            error_msg = "last name must be 3 or more"    
        elif not phone:
            error_msg = "Phone number is required !!"
        elif len(phone) < 10:
            error_msg = "Phone number must be 10 character long"
        elif not email:
            error_msg = "Email is required !!"
        elif len(email) < 5:
            error_msg = "Email must be 5 char long"
        elif not password:
            error_msg = "Password is required !!"
        elif len(password) < 6:
            error_msg = "Password must be 6 char long"
        elif Customer.objects.filter(email = email):
            data = Customer.objects.filter(email = email)
            print(f"Data is ==== {data}")
            error_msg = "Email address already registered !!"

        if not error_msg:
            customer = Customer(
                fname=fname,
                lname=lname,
                phone=phone,
                email=email,
                password=password 
            )
            customer.password = make_password(customer.password)
            customer.save()
            print("Registration successfully.........")
            return redirect('login')
        else:
            data = {
                "error":error_msg,
                "values":value
            }
            return render(request, 'signup.html',data)