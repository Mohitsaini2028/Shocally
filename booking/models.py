from django.db import models
from shop.models import Seller, User
from django.utils.timezone import now
# Create your models here.

class BookingItem(models.Model):
    item_id = models.AutoField
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE) # one to many relationship
    item_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subCategory = models.CharField(max_length=50, default="")
    originalPrice = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    desc = models.TextField()
    image = models.ImageField(upload_to='shop/images', default="")
    rating = models.FloatField(default=0.0)
    ratingNo = models.IntegerField(default=0)  #Number of rating by users



    def __str__(self):
             return self.item_name + " " + self.subCategory + " -- " + str(self.seller)
#shop m member bhi dalna



class TimeSlot(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE) # one to many relationship
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    max_booking = models.IntegerField(default=0)             #how many person can book at that time/slot
    bookingDate = models.DateField(auto_now_add=True,blank=True)

    def __str__(self):
        return str(self.starting_time) + " - " + str(self.ending_time) + " -- " + str(self.seller)


class Booking(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     item = models.ForeignKey(BookingItem,on_delete=models.CASCADE)
     time = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
     date = models.DateField()

     def __str__(self):
         return self.user.first_name + " " + self.user.last_name + " -- " + str(self.user.PINCODE)
