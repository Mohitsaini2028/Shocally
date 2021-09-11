from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.timezone import now

class User(AbstractUser):
    PINCODE=models.IntegerField(default=0)
    UserType=models.CharField(max_length=20, default="user")
    Address=models.CharField(max_length=500, default="")
    Category=models.CharField(max_length=50, default="")
    phoneNo=models.IntegerField(default=0)
    UserImg=models.ImageField(upload_to="shop/images",default="")

    is_Seller=models.BooleanField(default=False)
    is_Customer=models.BooleanField(default=False)
    is_Reporter=models.BooleanField(default=False)
    CityManager=models.BooleanField(default=False)

    @staticmethod
    def getUser(username):
        return User.objects.get(username=username)

    def __str__(self):
        return self.first_name+" "+self.last_name+" -- "+str(self.PINCODE)


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    PinCode=models.IntegerField(default=0)
    RatingGiven=models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+" -- "+str(self.user.PINCODE)

class Seller(models.Model): #Shop Information
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    RatingNo=models.IntegerField(default=0)
    PinCode=models.IntegerField(default=0)
    ShopName=models.CharField(max_length=100, default="")
    ShopCategory=models.CharField(max_length=50, default="")
    ShopAddress=models.CharField(max_length=500, default="")
    shopRating=models.IntegerField(default=0)
    longitude=models.FloatField(default=0.0)
    latitude=models.FloatField(default=0.0)
    ShopImg= models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " -- " + str(self.user.PINCODE) + " -  -  -  " + self.ShopCategory
