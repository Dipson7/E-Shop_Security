from django.contrib import admin
from .models import Product, Category, Customer, Orders
# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']    

class AdminCustomer(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'phone', 'email', 'password']    

class AdminOrders(admin.ModelAdmin):
    list_display = ['product','customer','quantity','price','phone','address']    

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Orders, AdminOrders)