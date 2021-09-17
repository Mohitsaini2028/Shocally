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

    def _str_(self):
        return self.first_name+" "+self.last_name+" -- "+str(self.PINCODE)


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    PinCode=models.IntegerField(default=0)
    RatingGiven=models.IntegerField(default=0)

    def _str_(self):
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

    def _str_(self):
        return self.user.first_name + " " + self.user.last_name + " -- " + str(self.user.PINCODE) + " -  -  -  " + self.ShopCategory


class Product(models.Model):
    product_id = models.AutoField
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)            # one to many relationship
    product_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subCategory = models.CharField(max_length=50, default="")
    originalPrice = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    desc = models.TextField()
    image = models.ImageField(upload_to='shop/images', default="")
    rating = models.FloatField(default=0.0)
    ratingNo = models.IntegerField(default=0)                             # Number of rating by users
    inStock = models.IntegerField(default=0)

    @property
    def updateRating(self,no):
        self.rating = (self.rating + no)/(ratingNo + 1)
        return self.rating

    @property
    def Save(self):
        return self.originalPrice - self.price

    @property
    def pinCode(self):
        return self.seller.PinCode

    @property
    def Discount(self):
        return 100-int((self.price/self.originalPrice)*100)

    def _str_(self):
        return self.product_name + "  ----  " + str(self.id)
