from django.contrib import admin
from .models import User, Customer, Seller, Product, Cart, Order, OrderUpdate, ProductRating, ShopRating, OrderNotification
from .forms import CustomerUserCreationForm
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    model=User
    add_form=CustomerUserCreationForm
    list_display =('username','id','first_name', 'last_name', 'PINCODE','is_Seller' ,'is_staff',)
    list_filter = ['is_Seller', 'is_Customer', 'is_Reporter', 'CityManager', 'groups', 'is_staff', 'is_superuser', 'is_active' ]

    add_fieldsets = UserAdmin.add_fieldsets + (
    (None, {'fields': ('email', 'first_name', 'last_name', 'PINCODE', 'UserType', 'Address', 'Category', 'PhoneNo', 'UserImg',)}),
    ('User role', {'fields': (  'is_Seller', 'is_Customer', )}),
    )

    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('PINCODE', 'UserType', 'Address', 'Category', 'PhoneNo', 'UserImg',)}),
    ('User role', {'fields': (  'is_Seller', 'is_Customer','is_Reporter','CityManager' )}),
    )



class ProductAdmin(admin.ModelAdmin):
     list_display=['product_name', 'price', 'subCategory', 'seller']
     search_fields = ['product_name','id', 'price', 'subCategory', 'category']

class SellerAdmin(admin.ModelAdmin):
     list_display=['user', 'shopName','id', 'shopCategory', 'pincode','productBased','appointmentBased']
     search_fields = [ 'shopName','id', 'shopCategory', 'pincode','productBased','appointmentBased']

admin.site.register(User,CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Seller,SellerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(ProductRating)
admin.site.register(OrderNotification)
admin.site.register(ShopRating)
