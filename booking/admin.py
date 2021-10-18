from django.contrib import admin
from .models import BookingItem, Booking, TimeSlot

# Register your models here.

admin.site.register(BookingItem)
admin.site.register(Booking)
admin.site.register(TimeSlot)
