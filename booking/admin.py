from django.contrib import admin
from .models import BookingItem, Booking, TimeSlot, BookingUpdate, BookingItemRating, BookingNotification

# Register your models here.

admin.site.register(BookingItem)
admin.site.register(Booking)
admin.site.register(TimeSlot)
admin.site.register(BookingUpdate)
admin.site.register(BookingItemRating)
admin.site.register(BookingNotification)
