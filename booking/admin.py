from django.contrib import admin
from .models import BookingItem, Booking, TimeSlot, BookingUpdate

# Register your models here.

admin.site.register(BookingItem)
admin.site.register(Booking)
admin.site.register(TimeSlot)
admin.site.register(BookingUpdate)
