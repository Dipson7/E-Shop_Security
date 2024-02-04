from django.contrib import admin
from django.urls import path
from .views import Index_page, user_signup, login_user, Cart_page, Checkout, Order_page
from .views import user_logout
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', Index_page.as_view(), name="index"),
    path('signup/', user_signup.as_view(), name='signup'),
    path('login/', login_user.as_view(), name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('cart/', Cart_page.as_view(), name='cart'),
    path('check-out/', Checkout.as_view(), name='checkout'),
    # path('orders/', Order_page.as_view(), name='orders')
    path('orders/', auth_middleware(Order_page.as_view()), name='orders')
]