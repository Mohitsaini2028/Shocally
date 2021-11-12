from django.shortcuts import render, HttpResponse,redirect, HttpResponseRedirect,reverse
from .models import  User, Seller, Reporter, News
from django.contrib.auth.hashers  import check_password,make_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def newsHome(request):
    if request.user.is_authenticated:
        pincode = request.user.PINCODE
    else:
        pincode = request.session.get('pincode',0)

    allNews = News.objects.filter(pincode=pincode,verified=True).order_by('-views')
    return render(request,'news/newsHome.html',{'allNews': allNews})

def newsView(request,newsId):
    news = News.objects.filter(id=newsId).first()

    allNews = News.objects.filter(verified=True)
    return render(request,'news/newsView.html',{'news':news})
