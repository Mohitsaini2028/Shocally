from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path("ShopView/<int:shopid>", views.shopView, name="shopView"),
    path("timeSlot/<int:shopid>", views.timeSlot, name="timeSlot"),    
    path("bookingItemView/<int:itemid>",views.bookingItemView, name="bookingItemView"),
    path("appointmentBook/", views.appointmentBook, name="appointmentBook"),
    path("appointmentNotify/<int:sellerId>", views.appointmentNotify, name="appointmentNotify"),
    path("ItemBookPage/<int:itemId>", views.ItemBookPage, name="ItemBookPage"),
    path('NewBookingItem/', views.NewBookingItem, name="NewBookingItem"),
    path('NewTimeSlot/', views.NewTimeSlot, name="NewTimeSlot"),
    path('editBookingItem/<int:bookId>', views.editBookingItem, name="editBookingItem"),
    path('editBookingItemHandle/', views.editBookingItemHandle, name="editBookingItemHandle"),
    path('bookingItemRatingUpdate/', views.bookingItemRatingUpdate, name="bookingItemRatingUpdate"),
    path('deleteBookingItem/',views.deleteBookingItem, name="deleteBookingItem"),
    path('update/', views.update, name="update"),


]
