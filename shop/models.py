from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.timezone import now

class User(AbstractUser):
    PINCODE=models.IntegerField(default=0)
    UserType=models.CharField(max_length=20, default="user")
    Address=models.CharField(max_length=500, default="")
    Category=models.CharField(max_length=50, default="")
    PhoneNo=models.IntegerField(default=0)
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
    pincode=models.IntegerField(default=0)
    ratingGiven=models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+" -- "+str(self.user.PINCODE)

class Seller(models.Model): #Shop Information
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ratingNo=models.IntegerField(default=0)
    pincode=models.IntegerField(default=0)
    shopName=models.CharField(max_length=100, default="")
    shopCategory=models.CharField(max_length=50, default="")
    shopAddress=models.CharField(max_length=500, default="")
    shopCity=models.CharField(max_length=150, default="")
    shopRating=models.IntegerField(default=0)
    views=models.IntegerField(default=0)
    longitude=models.FloatField(default=0.0)
    latitude=models.FloatField(default=0.0)
    shopImg= models.ImageField(upload_to="shop/images",default="")
    productBased=models.BooleanField(default=True)
    appointmentBased=models.BooleanField(default=False)

    #starting time ending time
    #no of workers

    def __str__(self):
        return self.shopName[:20].upper() + " "+ self.user.first_name + " " + self.user.last_name + " -- " + str(self.user.PINCODE) + " -  -  -  " + self.shopCategory


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
    def pincode(self):
        return self.seller.pincode

    @property
    def Discount(self):
        return 100-int((self.price/self.originalPrice)*100)

    def __str__(self):
        return self.product_name + "  ----  " + str(self.id)

class Cart(models.Model):
     user=models.OneToOneField(User,on_delete=models.CASCADE)
     itemJson=models.CharField(max_length=5000, default="")
     totalPrice=models.FloatField(default=0.0)
     totalCart=models.IntegerField(default=0)

     def __str__(self):
         return self.user.first_name + " " + self.user.last_name + " -- " + str(self.user.PINCODE)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    itemJson = models.CharField(max_length=5000)
    phoneNo=models.IntegerField(default=0)
    pincode=models.IntegerField(default=0)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    totalItem = models.IntegerField(default=0)
    totalPrice = models.FloatField(default=0.0)
    # country = models.CharField(max_length=111)

    def __str__(self):
        return self.itemJson[5:20] + "...       " + str(self.user) + str(self.user.username) 


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:25] + "...             " +"        Order ID : " +str(self.order_id)

class ProductRating(models.Model):
     rating=models.FloatField(default=0)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     comment=models.CharField(max_length=500,default="")

     def __str__(self):
        return str(self.user) + "   " + self.product.product_name[:10]+"...    Rating = "+ str(self.rating) +  "    Product Id - "+ str(self.product.id)

class ShopRating(models.Model):
     rating=models.FloatField(default=0)
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     shop=models.ForeignKey(Seller,on_delete=models.CASCADE)
     comment=models.CharField(max_length=500,default="")

     def __str__(self):
        return str(self.user) + "   " + self.shop.shopName[:10]+"...    Rating = "+ str(self.rating) +  "    Shop Id - "+ str(self.shop.id)


class OrderNotification(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notificatonJson = models.CharField(max_length=5000)
    def __str__(self):
        return str(self.seller) + " " + self.notificatonJson
