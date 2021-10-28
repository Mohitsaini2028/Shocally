from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth  import authenticate, login, logout
from .models import User, Seller, Customer, Product, Cart, Order, OrderUpdate, ProductRating
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from math import ceil
import json
from shop.forms import NewProductForm, NewSellerForm
import time
# Create your views here.

def home(request):
    return HttpResponse("<h1><i> hi home page </i></h1>")

def pincodeInput(request):
    return render(request, 'shop/pincode.html')

def pinResult(request,result):
    pincode=result
    allShop=[]
    prod=[]

    catprods = Seller.objects.values('shopCategory', 'id')
    cats = {item['shopCategory'] for item in catprods}

    for cat in cats:
        shop=Seller.objects.filter(pincode=pincode,shopCategory=cat,productBased=True,appointmentBased=False).order_by('-shopRating')
        if shop.exists():
            n = len(shop)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allShop.append([shop, range(1, nSlides), nSlides])

    params = {'allShop':allShop}

    return render(request, 'shop/index.html', params)

def pincodeResult(request):                                             #for those user who don't want to login
    pincode=request.GET['pinCode']
    return HttpResponseRedirect(f"/shop/pinResult/{pincode}")

def shopView(request,shopid):
    shop= Seller.objects.filter(id=shopid)
    allProds = []
    EXIST=[]

    catprods = Product.objects.values('subCategory', 'id')
    cats = {item['subCategory'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(seller=shop[0],subCategory=cat)
        if prod.exists():
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    print(allProds)
    if len(allProds)==0:
        prodExist=False
    else:
        prodExist=True

    form = NewProductForm()
    return render(request, 'shop/shopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist ,'form':form} )

def productView(request,prodid):
    product = Product.objects.filter(id=prodid)
    # recommendations = Product.objects.filter(category=product[0].category).order_by('-rating')
    # print(recommendations)
    recommendations = []

    # count = 0
    # for  i in Product.objects.filter(category=product[0].category,subCategory=product[0].subCategory).order_by('-rating'):
    #     if i.seller.Pincode == product[0].seller.Pincode:
    #             recommendations.append(i)
    #     if count>=5:
    #         break
    #     count+=1
    # seller.PinCode=product[0].seller.Pincode,

    # a=clusterRecommend.run(product[0].subCategory)
    # print(a)
    # suggestions = []
    # try:
    #     suggestions = aprori_recommender.run(product[0].subCategory)
    #     print("\n\n\n\n",suggestions)
    # except:
    #     print("\n\n\Exception occur at Aprori Recommendation System\n\n")
    return render(request, 'shop/prodView.html', {'product':product[0]})
    # return render(request, 'shop/prodView.html', {'product':product[0],'recommendations':recommendations,'suggestions':suggestions})


def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        pincode=request.POST['pinCode']
        phoneNo=request.POST['PhoneNo']


        userImg=request.FILES.get('userImg')
        address=request.POST['Address']

        UserType=request.POST['UserType']

        if 'Admin' in UserType:
            shopName=request.POST['shopName']
            shopCat=request.POST['shopCat']
            shopAddress=request.POST['shopAddress']
            shopImg=request.FILES.get('shopImg')
            BookingOrNot=bool(request.POST.get('BookingOrNot'))
            print("\n\n\n\n",BookingOrNot)
            if BookingOrNot:
                productBased=True
            else:
                productBased=False
            print(productBased,BookingOrNot)

        # check for errorneous input

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.set_password=pass1
        myuser.PINCODE= pincode
        myuser.PhoneNo= phoneNo
        myuser.UserImg= userImg
        myuser.Address= address

        if 'Admin' in UserType:
            myuser.UserType= UserType
            myuser.is_Seller=True
            myuser.is_Customer=False
            myuser.Category=shopCat
            mySeller=Seller.objects.create(user=myuser,shopName=shopName,pincode=pincode,shopCategory= shopCat,shopAddress=shopAddress,shopImg=shopImg,productBased=productBased,appointmentBased=BookingOrNot)
            myuser.save()
        else:
            myuser.UserType= 'User'
            myCustomer=Customer.objects.create(user=myuser,pincode=pincode)

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


def clearCart(request):
    cartUser= Cart.objects.filter(user=request.user.id)
    cartUser.update(itemJson="{}",totalPrice=0,totalCart=0)
    request.session['cartJson']=0
    request.session['cartPrice']=0
    request.session['cartTotal']=0

    print(request.user.id,request)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request,"shop/pincode.html")


def cart(request):
        user=request.POST['user']
        cartData=request.POST['cartData']
        cartUser = Cart.objects.filter(user=request.user.id)

        carts=json.loads(cartData)
        totalPrice=0
        totalCart=0
        for cart in carts:
            print(carts[cart][0],carts[cart][2])
            totalPrice+=carts[cart][0]*carts[cart][2]
            totalCart+=carts[cart][0]

        if cartUser:
            print(cartUser)
            cartUser.update(itemJson=cartData,totalPrice=totalPrice,totalCart=totalCart)
            print("- - - - - - - - - exist")
            request.session['cartJson']=cartUser[0].itemJson

        else:
            cartUser=Cart.objects.create(user=request.user,itemJson=cartData,totalPrice=totalPrice,totalCart=totalCart)
            cartUser.save()
            request.session['cartJson']=cartUser.itemJson

        # pr for product after pr the original id of product
        # productId : quantity ,product Name , product price(+discount)
        # {'pr3': [5, 'JBL partyBox', 9999], 'pr2': [3, 'mi band 3', 2000]}

        request.session['cartPrice']=totalPrice
        request.session['cartTotal']=totalCart

        return HttpResponse(cartData)


def newProduct(request):
    if request.method=='POST':
        form=NewProductForm(request.POST)
        product= Product()
        product.product_name=form.data['productName']
        product.category=form.data['category']
        product.subCategory=form.data['subCategory']
        product.originalPrice=form.data['originalPrice']
        product.price=form.data['price']
        product.desc=form.data['descripton']
        product.image=request.FILES.get('img')

        seller=Seller.objects.get(id=request.POST['sellerId'])
        product.seller=seller
        product.save()
        return HttpResponseRedirect(f"/shop/shopView/{request.POST['sellerId']}")

def editProduct(request,prodId):
    product=Product.objects.get(id=prodId)
    fields={'productName':product.product_name, 'category':product.category,'subCategory':product.subCategory,'originalPrice':product.originalPrice,'price':product.price,'descripton':product.desc,'img':product.image, 'inStock':product.inStock}
    form=NewProductForm(initial=fields)
    return  render(request, "shop/editProduct.html",{'form':form,'product':product})


def editProductHandle(request):
    if request.method=="POST":
        form=NewProductForm(request.POST)
        product=Product()
        oldProduct=Product.objects.get(id=request.POST['productId'])
        product.id=oldProduct.id
        product.product_name=form.data['productName']
        product.category=form.data['category']
        product.subCategory=form.data['subCategory']
        product.originalPrice=form.data['originalPrice']
        product.price=form.data['price']
        product.desc=form.data['descripton']
        product.inStock=form.data['inStock']
        if request.FILES.get('img'):
            product.image=request.FILES.get('img')
        else:
            product.image=oldProduct.image
        seller=Seller.objects.get(id=request.POST['sellerId'])
        product.seller=seller
        product.save()
    return HttpResponseRedirect(f"/shop/shopView/{request.POST['sellerId']}")

def editShop(request,sellId):
    seller=Seller.objects.get(id=sellId)
    fields={'pincode':seller.pincode, 'shopName':seller.shopName,'shopCategory':seller.shopCategory,'shopAddress':seller.shopAddress,'shopImg':seller.shopImg}
    form=NewSellerForm(initial=fields)
    return  render(request, "shop/editShop.html",{'form':form,'seller':seller})

def editShopHandle(request):
    if request.method=="POST":
        form=NewSellerForm(request.POST)
        seller=Seller()

        oldSeller=Seller.objects.get(id=request.POST['sellId'])
        seller.id=oldSeller.id
        seller.user=oldSeller.user
        seller.ratingNo=oldSeller.ratingNo
        seller.shopRating=oldSeller.shopRating
        seller.pincode=form.data['pincode']
        seller.shopName=form.data['shopName']
        seller.shopCategory=form.data['shopCategory']
        seller.shopAddress=form.data['shopAddress']
        if(request.FILES.get('shopImg')):
            seller.shopImg=request.FILES.get('shopImg')
        else:
            seller.shopImg=oldSeller.shopImg
        seller.save()
    return HttpResponseRedirect(f"/shop/shopView/{request.POST['sellId']}")



def placeOrder(request):
    cartUser= Cart.objects.get(user=request.user.id)
    user=User.objects.get(id=request.user.id)

    if cartUser.itemJson == "{}" and cartUser.totalPrice==0:
        messages.error(request,"please Add some items to the Cart. Your Cart is empty ")
        return HttpResponseRedirect(f"/shop/pinResult/{user.PINCODE}")
        # return HttpResponseRedirect(request.META['HTTP_REFERER'])

    print(user,user.PINCODE,cartUser)
    city=request.POST['city']
    if request.POST['address1'] == "":
        address=user.Address
    else:
        address=request.POST['address1']

    # sellerNotification = set()
    # obj = json.loads(cartUser.itemJson)
    # for reducing the stock in database
    # for key in obj:
    #     prodId = int(key[2:])
    #     prod=Product.objects.get(id=prodId)
    #     if prod.inStock>obj[key][0]:
    #             prod.inStock = prod.inStock - obj[key][0]
    #             sellerNotification.add(prod.seller)
    #     elif prod.inStock>0:
    #             prod.inStock = 0
    #             sellerNotification.add(prod.seller)
    #     else:
    #         pass  #if 0 present in stock
    #     prod.save()

        #for notify the seller
                                #seller information, demand, available


    # for i in  sellerNotification:
    #
    #     Dict = {} #for notificaton
    #     for key in obj:
    #          prodId = int(key[2:])
    #          prod=Product.objects.get(id=prodId)
    #          if i == prod.seller:
    #               # product id, name, price, demand, available
    #
    #              Dict.update({prod.id:[prod.product_name,prod.price,obj[key][0],prod.inStock]})
    #     notifyJson=json.dumps(Dict)
    #     orderNotify=orderNotification.objects.create(user=request.user, seller=i, notificatonJson=notifyJson)
    #     orderNotify.save()
    #
    # order=Order.objects.create(user=request.user,pincode=user.PINCODE,address=address,city=city,phoneNo=user.phoneNo,itemJson=cartUser.itemJson,totalPrice=cartUser.totalPrice,totalItem=cartUser.totalCart)
    # update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
    # order.save()
    # update.save()
    #
    # #adding data to dataset
    #
    #
    # prodList = []
    # setForCat = set()
    #
    # for key in obj:
    #     prodId = int(key[2:])
    #     prod=Product.objects.get(id=prodId)                 # product id
    #     cat = prod.category
    #     setForCat.add(cat)                                  # contain all unique category
    #     prodList.append(prod)
    #
    # for item in setForCat:
    #  rowUpdate = []
    #  rowUpdateCat = []
    #  for i in prodList:
    #         if i.category==item:
    #             rowUpdate.append(i.product_name.lower())            # list for row update
    #             rowUpdateCat.append(i.subCategory.lower())
    #         #          user ID, product ID, Seller ID, productName, productCategory, productSubCategory, productPrice,productDescription
    #         updateList([user.id,i.id,i.seller,i.product_name.lower(),i.category.lower(),i.subCategory.lower(),i.price,i.desc.lower()],'OrderFullDetail.csv')
    #  updateList(rowUpdate,'store_data1.csv')
    #  updateList(rowUpdateCat,'store_data1.csv')
    #
    #  rowUpdate.insert(0,user.id)
    #  rowUpdateCat.insert(0,user.id)
    #
    #  updateList(rowUpdate,'OrderDetail.csv')
    #  updateList(rowUpdateCat,'OrderDetail.csv')
    #

    cartUser.itemJson="{}"
    cartUser.totalPrice=0
    cartUser.totalCart=0
    cartUser.save()
    request.session['cartJson']=0
    request.session['cartPrice']=0
    request.session['cartTotal']=0
    messages.success(request,"Thankyou for Ordering From Shocally ")
    return HttpResponseRedirect(f"/shop/pinResult/{user.PINCODE}")




def checkout(request):
        return render(request, 'shop/checkout.html')

def tracker(request):
    orders=Order.objects.filter(user=request.user)
    orderUpdate=[]

    for order in orders:
        print("\n\n- - - - - - - ",order)
        update=OrderUpdate.objects.filter(order_id=order.order_id)
        if update:
            orderUpdate.append(update)
            print("\n\n - - - - - - - TRACKER- - - - - - - - \n\n")
    return render(request,'shop/tracker.html',{'orders':orders,'orderUpdate':orderUpdate})

def ratingPage(request,id):
    print("\n\n\n\n Rating Page")
    print(id)
    return render(request,'rating.html',{'id':id})

def prodRatingUpdate(request):
    id=request.user.id

    prod=Product.objects.get(id=request.POST['productId'])
    number=float(request.POST['RatingGiven'])
    print(type(number))
    print("\n\n\n\n")
    print("before",prod.rating,prod.ratingNo)
    prod.ratingNo+=1
    prod.rating = (prod.rating*(prod.ratingNo-1) + number)/prod.ratingNo
    print("after",prod.rating)
    time.sleep(2.4)

    prod.save()
    try:
        prodUpdate = ProductRating.objects.get(user=request.user,product=prod)
        #if user already rated the same product
        print("prodUpdate",prodUpdate)
        prodUpdate.rating=number
        prodUpdate.comment=request.POST['comment']
        prodUpdate.save()
        print(" Already Rated")
    except Exception as e:
        print("Exception hh bhai ",e)
        # if first time rating
        prodRat=ProductRating.objects.create(user=request.user,product=prod,rating=number,comment=request.POST['comment'])
        prodRat.save()
        print(" First Time Rated")

    return HttpResponseRedirect(f"/shop/productView/{request.POST['productId']}")


def handelLogin(request):
    if request.method=="POST":
        request.session.flush() #for if user try to login multiple times
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(request,username=loginusername, password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In")

            userCart= Cart.objects.filter(user=user)
            request.session['username']=loginusername
            if userCart:
                request.session['cartJson']=userCart[0].itemJson
                request.session['cartPrice']=userCart[0].totalPrice
                request.session['cartTotal']=userCart[0].totalCart

                print("- - - - - - - - - ",type(request.session['cartJson']))
            else:
                request.session['cartJson']=0
                request.session['cartPrice']=0
                request.session['cartTotal']=0
            if user.is_Seller:
                sellerUser=Seller.objects.filter(user=user)
                print(sellerUser[0].user.id)
                print(type(sellerUser[0].user.id))
                request.session['sellerUserId']=sellerUser[0].user.id #user
                request.session['shopId']=sellerUser[0].id #seller

            # request.session['user']=user #user is not serializeabe you can't pass it
            return HttpResponseRedirect(f"/shop/pinResult/{user.PINCODE}")

        else:

            messages.error(request, "LOGIN FAILED ! Invalid credentials! Please try again")
            return render(request,"shop/pincode.html")
            # return redirect("home")

    return HttpResponse("404- Not found")


def handelLogout(request):
    request.session.flush()
    logout(request)

    sytem_message=messages.get_messages(request)                                #for clear message you have to iterate
    for msg in sytem_message:
        print(sytem_message)

    # del request.session['username']
    messages.success(request, "Successfully logged out")
    return render(request,"shop/pincode.html")
