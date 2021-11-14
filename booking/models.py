from django.db import models
from shop.models import Seller, User
from django.utils.timezone import now
# Create your models here.

class BookingItem(models.Model):
    item_id = models.AutoField
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE) # one to many relationship
    service_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subCategory = models.CharField(max_length=50, default="")
    originalPrice = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    desc = models.TextField()
    image = models.ImageField(upload_to='booking/images', default="")
    rating = models.FloatField(default=0.0)
    ratingNo = models.IntegerField(default=0)  #Number of rating by users
    @property
    def updateRating(self,no):
        self.rating = (self.rating + no)/(ratingNo + 1)
        return self.rating

    @property
    def Save(self):
        return self.originalPrice - self.price

    @property
    def pincode(self):
        return self.seller.pincode

    @property
    def Discount(self):
        return 100-int((self.price/self.originalPrice)*100)

    def __str__(self):
        return self.service_name + "  ----  " + str(self.id)


    def __str__(self):
             return self.service_name + " " + self.subCategory + " -- " + str(self.seller)
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

     def __str__(self):
         return self.user.first_name + " " + self.user.last_name + " -- " + str(self.user.PINCODE)


class BookingUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:25] + "...             " +"        Order ID : " +str(self.booking_id)

class BookingItemRating(models.Model):
     rating=models.FloatField(default=0)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     bookingItem=models.ForeignKey(BookingItem,on_delete=models.CASCADE)
     comment=models.CharField(max_length=500,default="")

     def __str__(self):
        return str(self.user) + "   " + self.bookingItem.service_name[:10]+"...    Rating = "+ str(self.rating) +  "    BookingItem Id - "+ str(self.bookingItem.id)

class AppointmentNotification(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notificatonJson = models.CharField(max_length=5000)
    def __str__(self):
        return str(self.seller) + " " + self.notificatonJson
