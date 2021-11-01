from django.contrib import admin
from .models import User, Customer, Seller, Product, Cart, Order, OrderUpdate, ProductRating, ShopRating
from .forms import CustomerUserCreationForm
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    model=User
    add_form=CustomerUserCreationForm
    list_display =('username','id','first_name', 'last_name', 'PINCODE','is_Seller' ,'is_staff',)

    add_fieldsets = UserAdmin.add_fieldsets + (
    (None, {'fields': ('email', 'first_name', 'last_name', 'PINCODE', 'UserType', 'Address', 'Category', 'PhoneNo', 'UserImg',)}),
    ('User role', {'fields': (  'is_Seller', 'is_Customer', )}),
    )

    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('PINCODE', 'UserType', 'Address', 'Category', 'PhoneNo', 'UserImg',)}),
    ('User role', {'fields': (  'is_Seller', 'is_Customer','is_Reporter','CityManager' )}),
    )


admin.site.register(User,CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(ProductRating)
admin.site.register(ShopRating)
