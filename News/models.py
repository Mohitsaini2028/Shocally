from django.db import models
from shop.models import User, Seller, Product, Customer, Cart, Order, OrderUpdate
from django.utils.timezone import now
from ckeditor.fields import RichTextField

# Create your models here.


class Reporter(models.Model):
      user=models.OneToOneField(User,on_delete=models.CASCADE)
      RatingGiven=models.IntegerField(default=0)
      NewsCompany=models.CharField(max_length=100, default="")
      def __str__(self):
          return self.user.first_name+" "+self.user.last_name +" "+ str(self.user.PINCODE)

class News(models.Model):
    pincode=models.IntegerField(default=0)
    publisher=models.ForeignKey(Reporter,on_delete=models.CASCADE) # one to many relationship
    newsHeadline=models.CharField(max_length=60, default="")
    newsCategory=models.CharField(max_length=20, default="")
    news=RichTextField(max_length=15000, default="")
    time=models.DateTimeField(default=now)
    verified=models.BooleanField(default=False)
    image= models.ImageField(upload_to="news/images",default="")
    views= models.IntegerField(default=0)

    def __str__(self):
        return self.newsHeadline+" "+"by"+" --  "+self.publisher.user.first_name+" "+self.publisher.user.last_name
