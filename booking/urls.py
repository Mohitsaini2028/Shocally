from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path("ShopView/<int:shopid>", views.shopView, name="shopView"),
    path("appointmentBook/", views.appointmentBook, name="appointmentBook"),
    path("ItemBookPage/<int:itemId>", views.ItemBookPage, name="ItemBookPage"),
    path('NewBookingItem/', views.NewBookingItem, name="NewBookingItem"),

]
