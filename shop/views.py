from django.shortcuts import render,HttpResponse,redirect
# Create your views here.

def home(request):
    return HttpResponse("<h1><i> hi home page </i></h1>")

def pincodeInput(request):
    return render(request, 'pincode.html')

def pinResult(request):
    pinCode=request.GET['pinCode']
    return render(request, 'pincode.html',{'pinCode':pinCode})
