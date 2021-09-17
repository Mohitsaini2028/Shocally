from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth  import authenticate, login, logout
from .models import User, Seller, Customer
from django.contrib import messages
# Create your views here.

def home(request):
    return HttpResponse("<h1><i> hi home page </i></h1>")

def pincodeInput(request):
    return render(request, 'pincode.html')

def pinResult(request):
    pinCode=request.GET['pinCode']
    return render(request, 'pincode.html',{'pinCode':pinCode})

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        PinCode=request.POST['pinCode']
        PhoneNo=request.POST['PhoneNo']

        userImg=request.FILES.get('userImg')
        Address=request.POST['Address']

        UserType=request.POST['UserType']

        if 'Admin' in UserType:
            shopName=request.POST['shopName']
            shopCat=request.POST['shopCat']
            shopAddress=request.POST['shopAddress']
            shopImg=request.FILES.get('shopImg')



        # check for errorneous input

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.set_password=pass1
        myuser.PINCODE= PinCode
        myuser.phoneNo= PhoneNo
        myuser.UserImg= userImg
        myuser.Address= Address

        if 'Admin' in UserType:
            myuser.UserType= UserType
            myuser.is_Seller=True
            myuser.is_Customer=False
            myuser.Category=shopCat
            mySeller=Seller.objects.create(user=myuser,ShopName=shopName,PinCode=PinCode,ShopCategory= shopCat,ShopAddress= shopAddress,ShopImg= shopImg)
            myuser.save()
        else:
            myuser.UserType= 'User'
            myCustomer=Customer.objects.create(user=myuser,PinCode=PinCode)

        myuser.save()
        if myuser.is_Seller:
            messages.success(request, " Your Shocally Seller Account has been successfully created")
        else:
            messages.success(request, " Your Shocally Customer Account has been successfully created")

        request.session['cartJson']=0
        request.session['cartPrice']=0
        request.session['cartTotal']=0
        login(request,myuser)
        return HttpResponseRedirect(f"/pinResult/{myuser.PINCODE}")


    else:
        messages.error("Invalid credentials !! Please try again ")
        return redirect('home')
