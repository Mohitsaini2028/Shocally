from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth  import authenticate, login, logout
from .models import User, Seller, Customer, Product, Cart, Order, OrderUpdate, ProductRating, ShopRating
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from math import ceil
import json
from shop.forms import NewProductForm, NewSellerForm
import time
import csv
from pathlib import Path
import os
from Recommendation.Association import aprori_recommender
from Recommendation.Clustering import clusterRecommend
from AdvanceSearch import advance_search_functionality as search_check


BASE_DIR = Path(__file__).resolve().parent.parent
recommendations_path=os.path.join(BASE_DIR,'Recommendation')
advance_search_path=os.path.join(BASE_DIR,'AdvanceSearch')
# Create your views here.

#updating file for Search Term
def updateDataFile(lis):
    with open(advance_search_path+'\\data.csv','a',encoding="utf-8",newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(lis)
        f_object.close()

def updateSearchFile(request):
    products=Product.objects.all()
    for i in products:
        lis = [i.category,i.category,1.0]
        updateDataFile(lis)
        lis = [i.subCategory,i.subCategory,1.0]
        updateDataFile(lis)

    return HttpResponse("<h1>File Updated!!</h1>")

def home(request):
    return HttpResponse("<h1><i> hi home page </i></h1>")

def pincodeInput(request):
    return render(request, 'homePage.html')

def exampleHomePage(request):
    return render(request,'homePage.html')

def search(request):
    return render(request,"search.html")

def advanceSearch(query):

    with open(advance_search_path+'\\data.csv', "r") as f:
        word = f.read().split(",")

    #from fuzzywuzzy import process
    from fuzzywuzzy import fuzz, process

    '''
    soundex = fuzz.Soundex(10)
    # Text to process
    word = 'phone'
    soundex(word)
    '''

    def get_matches(query, choices, limit=3):
            results = process.extract(query, choices, limit=limit)
            return results

    '''
    try to apply sorting features for on higher to lower order aur on the basic of date

    agar data extract karne par 0 ya 5 s kam matching nikle toh fir word ko match karna fir wapis s fetch karna database s

    '''

    match=get_matches(f"{query}", word)


    return match

def querySetGetter(query,pincode,category): 
        if category=='product':
            allProductName= Product.objects.filter(product_name__icontains=query,seller__pincode=pincode)
            allProductCategory= Product.objects.filter(category__icontains=query,seller__pincode=pincode)
            allProductSubCategory =Product.objects.filter(subCategory__icontains=query,seller__pincode=pincode)
            allProduct=  allProductName.union(allProductCategory, allProductSubCategory)
            return allProduct



def searchResult(request):
    query = request.POST.get('query')
    #category = request.POST.get('category')
    category = 'product'
    if request.user.is_authenticated:
        pincode = request.user.PINCODE
    else:
        pincode = request.session.get('pincode',0) #setting default value 0 when user did't provide the pincode.
    sliced = search_check.main(query)
    if sliced[2].upper() in termFilter.keys():
                try:
                   
                    productResult=operations[sliced[2].upper()](sliced[0][0])(sliced[1])
                    params={'allProduct': productResult, 'query': query}
                    print(query,allProduct)
                    return render(request,"searchResult.html",params)
                    
                    
                except:
                    messages.warning(request, "No search results found. Please refine your query.")
                    params={'allProduct': Product.objects.none(), 'query': query}
                    print(query,allProduct)
                    return render(request,"searchResult.html",params)
    
    '''
    s=advanceSearch(query)
    result = []

    for item in s:
        res=''.join([i for i in item[0] if not i.isdigit()])
        if res.startswith('.\n'):
            res=res[2:]
        result.append(res)
        
    
        
    print("\n\n\n\n",result)
    '''

    if len(query)>78 and len(query)<=1:
        allProduct=Product.objects.none()
    else:
        allProductName= Product.objects.filter(product_name__icontains=query,seller__pincode=pincode)

        allProductCategory= Product.objects.filter(category__icontains=query,seller__pincode=pincode)
        allProductSubCategory =Product.objects.filter(subCategory__icontains=query,seller__pincode=pincode)
        allProduct=  allProductName.union(allProductCategory, allProductSubCategory)
        print(type(allProduct))

    if allProduct.count()==0:
        #if User type the search Term Incorrectly.
        '''
        if len(query)<78 and len(query)>1 :
                s=advanceSearch(query)
                result = []

                for item in s:
                    res=''.join([i for i in item[0] if not i.isdigit()])
                    if res.startswith('.\n'):
                        res=res[2:]
                    result.append(res)
                
                #if you want all term matching result
                for i in result:
                    queryset=querySetGetter(i,pincode,category)
                    allProduct=allProduct.union(queryset)
                
                #if you only want only first term matching result
                #allProduct=querySetGetter(i,pincode,category)
           
        
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allProduct': allProduct, 'query': query}
    print(query,allProduct)
    return render(request,"searchResult.html",params)


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
    request.session['pincode']=pincode
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
        prod = Product.objects.filter(seller=shop[0],subCategory=cat).order_by('-rating')
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

    recommendations = []

    count = 0
    for  i in Product.objects.filter(category__iexact=product[0].category,subCategory__iexact=product[0].subCategory).exclude(id=product[0].id).order_by('-rating'):
        print("\n\n\n\nRecommendation i",i)
        if i.seller.pincode == product[0].seller.pincode:
                recommendations.append(i)
        if count>=5:
            break
        count+=1



    clusters = clusterRecommend.run(product[0].subCategory.lower())



    suggestions=[]


    result = aprori_recommender.run(product[0].subCategory.lower())
    print("RESULT APPRORI RECOMMENDER : ",result)
    result = (clusters + list(set(result) - set(clusters)))
    print("RESULT APPRORI RECOMMENDER : ",result)
    if result:

                    for i in result:
                        print(i)
                        for  j in Product.objects.filter(category=product[0].category,subCategory__icontains=i).exclude(id=product[0].id).order_by('-rating'):
                            print(",",j)
                            if j.seller.pincode == product[0].seller.pincode:
                                    suggestions.append(j)

    print("\n\n\n\n",suggestions)

    n = len(suggestions)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))


    # print(e, "\n\n\Exception occur at Aprori Recommendation System\n\n")
    return render(request, 'shop/prodView.html', {'product':product[0],'recommendations':recommendations,'suggestions':suggestions,'range':range(1, nSlides) })


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
                productBased=False
            else:
                productBased=True
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

@login_required(login_url='/')
def clearCart(request):
    cartUser= Cart.objects.filter(user=request.user.id)
    cartUser.update(itemJson="{}",totalPrice=0,totalCart=0)
    request.session['cartJson']=0
    request.session['cartPrice']=0
    request.session['cartTotal']=0

    print(request.user.id,request)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request,"homePage.html")

@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
def editProduct(request,prodId):
    product=Product.objects.get(id=prodId)
    fields={'productName':product.product_name, 'category':product.category,'subCategory':product.subCategory,'originalPrice':product.originalPrice,'price':product.price,'descripton':product.desc,'img':product.image, 'inStock':product.inStock}
    form=NewProductForm(initial=fields)
    return  render(request, "shop/editProduct.html",{'form':form,'product':product})

@login_required(login_url='/')
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

@login_required(login_url='/')
def deleteProduct(request):
    prodId=int(request.POST['delProd'])
    sellerId=int(request.POST['sellerId'])
    print(sellerId," a rha h yrr yha tak")
    product=Product.objects.get(id=prodId)
    product.delete()
    messages.success(request, "Product is successfully deleted")
    return HttpResponseRedirect(f"/shop/shopView/{sellerId}")

@login_required(login_url='/')
def editShop(request,sellId):
    seller=Seller.objects.get(id=sellId)
    fields={'pincode':seller.pincode, 'shopName':seller.shopName,'shopCategory':seller.shopCategory,'shopAddress':seller.shopAddress,'shopImg':seller.shopImg}
    form=NewSellerForm(initial=fields)
    return  render(request, "shop/editShop.html",{'form':form,'seller':seller})

@login_required(login_url='/')
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


@login_required(login_url='/')
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
    order=Order.objects.create(user=request.user,pincode=user.PINCODE,address=address,city=city,phoneNo=user.PhoneNo,itemJson=cartUser.itemJson,totalPrice=cartUser.totalPrice,totalItem=cartUser.totalCart)
    update = OrderUpdate.objects.create(order_id=order.order_id, update_desc="The order has been placed")
    order.save()
    update.save()
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

@login_required(login_url='/')
def checkout(request):
        return render(request, 'shop/checkout.html')

@login_required(login_url='/')
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


@login_required(login_url='/')
def ratingPage(request,id,val):
    print("\n\n\n\n Rating Page")
    print(id,"val",val)
    if val=="product":
        return render(request,'rating.html',{'id':id,'url':"/shop/prodRatingUpdate/"})
    elif val=="shop":
        return render(request,'rating.html',{'id':id,'url':"/shop/shopRatingUpdate/"})
    elif val=="booking":
        return render(request,'rating.html',{'id':id,'url':"/booking/bookingItemRatingUpdate/"})

@login_required(login_url='/')
def shopRatingUpdate(request):
    id=request.user.id

    shop=Seller.objects.get(id=request.POST['Id'])
    number=float(request.POST['RatingGiven'])
    print(type(number))
    print("\n\n\n\n")
    print("before",shop.shopRating,shop.ratingNo)
    shop.ratingNo+=1
    shop.shopRating = (shop.shopRating*(shop.ratingNo-1) + number)/shop.ratingNo
    print("after",shop.shopRating)
    time.sleep(2.4)

    shop.save()
    try:
        shopUpdate = ShopRating.objects.get(user=request.user,shop=shop)
        #if user already rated the same product
        print("shopUpdate",shopUpdate)
        shopUpdate.shopRating=number
        shopUpdate.comment=request.POST['comment']
        shopUpdate.save()
        print(" Already Rated")
    except Exception as e:
        print("Exception Rating Page",e)
        # if first time rating
        shopRat=ShopRating.objects.create(user=request.user,shop=shop,rating=number,comment=request.POST['comment'])
        shopRat.save()
        print(" First Time Rated")

    with open(recommendations_path+'\\shopRating.csv','a') as f_object:
        writer_object = csv.writer(f_object)
        print("writing data in csv file.")
        writer_object.writerow([request.user.id,request.POST['Id'],number,1395578400])
        f_object.close()

    return HttpResponseRedirect(f"/shop/shopView/{request.POST['Id']}")

@login_required(login_url='/')
def prodRatingUpdate(request):
    id=request.user.id

    prod=Product.objects.get(id=request.POST['Id'])
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
        print("Exception Rating Page",e)
        # if first time rating
        prodRat=ProductRating.objects.create(user=request.user,product=prod,rating=number,comment=request.POST['comment'])
        prodRat.save()
        print(" First Time Rated")

    #writing data in csv file.
    with open(recommendations_path+'\\rating.csv','a') as f_object:
        writer_object = csv.writer(f_object)
        print("writing data in csv file.")
        writer_object.writerow([request.user.id,request.POST['Id'],number,1395578400])
        f_object.close()

    return HttpResponseRedirect(f"/shop/productView/{request.POST['Id']}")


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
                request.session['appointmentBased']=sellerUser[0].appointmentBased #seller

            # request.session['user']=user #user is not serializeabe you can't pass it
            return HttpResponseRedirect(f"/shop/pinResult/{user.PINCODE}")

        else:

            messages.error(request, "LOGIN FAILED ! Invalid credentials! Please try again")
            return render(request,"homePage.html")
            # return redirect("home")

    return HttpResponse("404- Not found")

@login_required(login_url='/')
def handelLogout(request):
    request.session.flush()
    logout(request)

    sytem_message=messages.get_messages(request)                                #for clear message you have to iterate
    for msg in sytem_message:
        print(sytem_message)

    # del request.session['username']
    messages.success(request, "Successfully logged out")
    return render(request,"homePage.html")
