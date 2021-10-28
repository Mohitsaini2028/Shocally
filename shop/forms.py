from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields="__all__"

class NewProductForm(forms.Form):
    productName = forms.CharField(max_length=50)
    category = forms.CharField(max_length=50)
    subCategory=forms.CharField(max_length=50)
    originalPrice = forms.FloatField()
    price = forms.FloatField()
    descripton = forms.CharField(widget=forms.Textarea)
    img = forms.ImageField()
    inStock = forms.IntegerField()

class NewSellerForm(forms.Form):
    pincode=forms.IntegerField()
    shopName=forms.CharField(max_length=100)
    shopCategory=forms.CharField(max_length=50)
    shopAddress=forms.CharField(max_length=500)
    shopImg= forms.ImageField()
