from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth  import authenticate, login, logout
from .models import User, Seller, Customer, Product, Cart, Order, OrderUpdate, ProductRating, ShopRating, OrderNotification
from News.models import News, Reporter
from booking.models import BookingItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from math import ceil
import json
from shop.forms import NewProductForm, NewSellerForm
import time
import csv
from pathlib import Path
import os
from Recommendation import recommender
from Recommendation.Association import aprori_recommender
from Recommendation.Clustering import clusterRecommend
from AdvanceSearch import advance_search_functionality as search_check
from FakeViewCounter import currentdate


BASE_DIR = Path(__file__).resolve().parent.parent
recommendations_path=os.path.join(BASE_DIR,'Recommendation')
advance_search_path=os.path.join(BASE_DIR,'AdvanceSearch')
fake_view_counter_path=os.path.join(BASE_DIR,'FakeViewCounter')

# Create your views here.

def error(request,string):
    return HttpResponse("<h1>404 NOT FOUND!!</h1>")

#updating file for Search Term
def updateDataFile(lis):
    # with open(advance_search_path+'\\search_term.csv','a',encoding="utf-8",newline='') as f_object:
    with open(advance_search_path+'\\data.csv','a',encoding="utf-8",newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(lis)
        f_object.close()

def updateList(lis,fileName):
    with open(recommendations_path+'\\Association\\'+str(fileName),'a',newline='',encoding="utf-8") as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(lis)

def updateCity(request):
    sellers=Seller.objects.all()
    city = { 458441: 'Neemuch', 452001: 'Indore' , 332713: 'Neem Ka Thana', 473446: 'Chanderi'}
    for i in sellers:
        i.shopCity = city[i.pincode]
        i.save()
    return HttpResponse("<h1>City Updated Successfully !!</h1>")

def updateSearchFile(request):
    products=Product.objects.all()
    for i in products:
        lis = [i.category,i.category,1.0]
        updateDataFile(lis)
        lis = [i.subCategory,i.subCategory,1.0]
        updateDataFile(lis)

    return HttpResponse("<h1>File Updated!!</h1>")

def about(request):
    return render(request,"about.html")

def ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR') #client ip Address
    print(ip)
    return ip

def updateViews(request):
    #cron job  #for updating views

    lis = ['shop','news']
    # '''
    for item in lis:
        if item == 'shop':
             id_views = currentdate.check_occurrences(item)
             for key, value in id_views.items():
                shop = Seller.objects.get(id=key)
                shop.views += value
                shop.save()
                print("VIEW UPDATED : ",key,value)

    return HttpResponse("<h1>VIEW UPDATED !!</h1>")
    # '''
    # pass

def aboveResult(term,number,pincode):
        allProductName= Product.objects.filter(product_name__icontains=term,price__gte=number,seller__pincode=pincode)
        allProductCategory= Product.objects.filter(category__icontains=term,price__gte=number,seller__pincode=pincode)
        allProductSubCategory =Product.objects.filter(subCategory__icontains=term,price__gte=number,seller__pincode=pincode)
        allProduct =  allProductName.union(allProductCategory, allProductSubCategory)
        print("Above Product Result",allProduct)
        return allProduct

def belowResult(term,number,pincode):
        allProductName= Product.objects.filter(product_name__icontains=term,price__lte=number,seller__pincode=pincode)
        allProductCategory= Product.objects.filter(category__icontains=term,price__lte=number,seller__pincode=pincode)
        allProductSubCategory =Product.objects.filter(subCategory__icontains=term,price__lte=number,seller__pincode=pincode)
        allProduct =  allProductName.union(allProductCategory, allProductSubCategory)
        print("Below Product Result",allProduct)
        return allProduct


termFilter={"ABOVE":aboveResult, "MINIMUM":aboveResult ,"MIN":aboveResult, "BELOW":belowResult , "UNDER":belowResult, "MAXIMUM":belowResult, "MAX":belowResult}

def home(request):
    return HttpResponse("<h1><i> hi home page </i></h1>")

def pincodeInput(request):
    return render(request, 'homePage.html')

def exampleHomePage(request):
    return render(request,'homePage.html')

def search(request):
    return render(request,"search.html")

def advanceSearch(query):

    # with open(advance_search_path+'\\search_term.csv', "r") as f:
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
            print("querySetGetter  Product")
            allProductName= Product.objects.filter(product_name__icontains=query,seller__pincode=pincode)
            allProductCategory= Product.objects.filter(category__icontains=query,seller__pincode=pincode)
            allProductSubCategory =Product.objects.filter(subCategory__icontains=query,seller__pincode=pincode)
            allProduct=  allProductName.union(allProductCategory, allProductSubCategory)
            return allProduct

        if category=='shop':
            print("querySetGetter  Shop")                                        #note you should check if it is product based shop or booking type
            allShopName = Seller.objects.filter(shopName__icontains=query,pincode=pincode)
            allCategory = Seller.objects.filter(shopCategory__icontains=query,pincode=pincode)
            allAddress = Seller.objects.filter(shopAddress__icontains=query,pincode=pincode)
            allShop =  allShopName.union(allCategory, allAddress)
            return allShop

        if category=='news':                                         #note you should check if it is product based shop or booking type
            print("querySetGetter  News",query)
            allHeadlines = News.objects.filter(newsHeadline__icontains=query,pincode=pincode)
            allCategory = News.objects.filter(newsCategory__icontains=query,pincode=pincode)
            allNew = News.objects.filter(news__icontains=query,pincode=pincode)
            allNews =  allHeadlines.union(allCategory, allNew)
            print(allNews)
            return allNews

        if category=='booking':                                         #note you should check if it is product based shop or booking type
            print("querySetGetter  booking",query)
            allServiceName = BookingItem.objects.filter(service_name__icontains=query,seller__pincode=pincode)
            allCategory = BookingItem.objects.filter(category__icontains=query,seller__pincode=pincode)
            allsubCategory = BookingItem.objects.filter(subCategory__icontains=query,seller__pincode=pincode)
            allBooking =  allServiceName.union(allServiceName, allsubCategory)
            print(allBooking)
            return allBooking


def searchResult(request):
    query = request.POST.get('query')
    cat = request.POST.get('cat')
    pincode = request.POST.get('pin')

    category = cat.lower()
    print("\n\n\n\nCategory",category   )
    #category = request.POST.get('category')

    # category = 'shop'
    # category = 'booking'
    if request.user.is_authenticated:
        # pincode = request.user.PINCODE
        pincode = pincode
    else:
        # pincode = request.session.get('pincode',0) #setting default value 0 when user did't provide the pincode.
        pincode = pincode

    sliced = False
    if category == 'product':
        for word in query.split(' '):
            if word.upper() in termFilter.keys():
                sliced = True

    elif category == 'news':
        pass

    productResult = []

    if sliced:
        sliced = search_check.main(query)
        print("Result operations ",sliced)
        if sliced[0][0].upper() in termFilter.keys():
                try:

                    productResult=termFilter[sliced[0][0].upper()](sliced[2][0],sliced[1][0],pincode)
                    params={'allProduct': productResult, 'query': query}
                    print(query,productResult)
                    return render(request,"searchResult.html",params)


                except Exception as e:
                    print("Exception ",e)
                    messages.warning(request, "No search results found. Please refine your query.")
                    params={'allProduct': Product.objects.none(), 'query': query}
                    # print(query,allProduct)
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

    print(query)
    if len(query)>78 or len(query)<=1:
        print("Query length")
        querysetResult=Product.objects.none()
    else:
        querysetResult=querySetGetter(query,pincode,category)


    if querysetResult.count()==0:
        #if User type the search Term Incorrectly.
        #'''
        if len(query)<78 and len(query)>1 :
                s=advanceSearch(query)
                print("PHONETIC SEARCH RESULT",s)
                result = []

                for item in s:
                    res=''.join([i for i in item[0] if not i.isdigit()])
                    if res.startswith('.\n'):
                        res=res[2:]
                    result.append(res)

                #if you want all term matching result
                for i in result:
                    queryset=querySetGetter(i,pincode,category)
                    querysetResult=querysetResult.union(queryset)

                #if you only want only first term matching result
                #allProduct=querySetGetter(i,pincode,category)
        #'''
        else:
           messages.warning(request, "No search results found. Please refine your query.")

    if category=='product':
        params={'allProduct': querysetResult, 'query': query}
        print("Product Search ", query,querysetResult)
    elif category=='shop':
        params={'allShop': querysetResult, 'query': query}
        print("Shop Search ",query,params)
    elif category=='news':
        params={'allNews': querysetResult, 'query': query}
        print("News Search ",query,params)
    elif category=='booking':
        params={'allBooking': querysetResult, 'query': query}
        print("Booking Search ",query,params)
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

    #'''
    recommend = []
    if request.user.is_authenticated:
        userID = request.user.id
        num_recommendations = 10
        try:
            # rec = recommender.recommend_items(userID, recommender.pivot_df, recommender.preds_df, num_recommendations)
            rec = recommender.recommendPass(userID,num_recommendations)
            for id in rec:
                print(id,type(id))
                prod = Product.objects.filter(id = id).first()
                if prod:
                    recommend.append(prod)
        except Exception as e:
            print("\n\n\n\n Exception Recommendation",e)
            #if user is new or user didn't gave any rating to any product



    print(recommend)
    if len(recommend)>0:
        n = len(recommend)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

    params = {'allShop':allShop,'recommend':recommend,'nSlides':nSlides}
    #'''
    #params = {'allShop':allShop}
    request.session['pincode']=pincode
    return render(request, 'shop/index.html', params)

def cityResult(request,stringResult):
    city=stringResult
    allShop=[]
    prod=[]

    catprods = Seller.objects.values('shopCategory', 'id')
    cats = {item['shopCategory'] for item in catprods}

    pincode = 0

    for cat in cats:
        shop=Seller.objects.filter(shopCity__iexact=city,shopCategory=cat,productBased=True,appointmentBased=False).order_by('-shopRating')
        if shop.exists():
            pincode = shop[0].pincode
            n = len(shop)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allShop.append([shop, range(1, nSlides), nSlides])

    #'''
    recommend = []
    if request.user.is_authenticated:
        userID = request.user.id
        num_recommendations = 10
        try:
            # rec = recommender.recommend_items(userID, recommender.pivot_df, recommender.preds_df, num_recommendations)
            rec = recommender.recommendPass(userID,num_recommendations)
            for id in rec:
                print(id,type(id))
                prod = Product.objects.filter(id = id).first()
                if prod:
                    recommend.append(prod)
        except Exception as e:
            print("\n\n\n\n Exception Recommendation",e)
            #if user is new or user didn't gave any rating to any product



    print(recommend)
    if len(recommend)>0:
        n = len(recommend)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

    params = {'allShop':allShop,'recommend':recommend,'nSlides':nSlides}
    #'''
    #params = {'allShop':allShop}
    request.session['pincode']=pincode
    return render(request, 'shop/index.html', params)




def pincodeResult(request):                                             #for those user who don't want to login
    pincode=request.GET['pinCode']
    if pincode.isnumeric():
        return HttpResponseRedirect(f"/shop/pinResult/{pincode}")
    else:
        return HttpResponseRedirect(f"/shop/cityResult/{pincode}")


def shopView(request,shopid):

    ipAddress=ip(request)
    print(ipAddress)
    currentdate.update_ip('shop',ipAddress,shopid)

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
    suggestions=[]
    '''
    nSlides = 0
    '''

    count = 0
    #'''
    for  i in Product.objects.filter(category__iexact=product[0].category,subCategory__iexact=product[0].subCategory).exclude(id=product[0].id).order_by('-rating'):
        print("\n\n\n\nRecommendation i",i)
        if i.seller.pincode == product[0].seller.pincode:
                recommendations.append(i)
        if count>=5:
            break
        count+=1



    clusters = clusterRecommend.run(product[0].subCategory.lower())






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
    #'''
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

    sellerNotification = set()
    obj = json.loads(cartUser.itemJson)
    # for reducing the stock in database
    for key in obj:
        prodId = int(key[2:])
        prod=Product.objects.get(id=prodId)
        if prod.inStock>obj[key][0]:
                prod.inStock = prod.inStock - obj[key][0]
                sellerNotification.add(prod.seller)
        elif prod.inStock>0:
                prod.inStock = 0
                sellerNotification.add(prod.seller)
        else:
            pass  #if 0 present in stock
        prod.save()

        #for notify the seller
                                #seller information, demand, available


    for i in  sellerNotification:

        Dict = {} #for notificaton
        for key in obj:
             prodId = int(key[2:])
             prod=Product.objects.get(id=prodId)
             if i == prod.seller:
                  # product id, name, price, demand, available

                 Dict.update({prod.id:[prod.product_name,prod.price,obj[key][0],prod.inStock]})
        notifyJson=json.dumps(Dict)
        orderNotify=OrderNotification.objects.create(user=request.user, seller=i, notificatonJson=notifyJson)
        orderNotify.save()

    order=Order.objects.create(user=request.user,pincode=user.PINCODE,address=address,city=city,phoneNo=user.PhoneNo,itemJson=cartUser.itemJson,totalPrice=cartUser.totalPrice,totalItem=cartUser.totalCart)
    update = OrderUpdate.objects.create(order_id=order.order_id, update_desc="The order has been placed")
    order.save()
    update.save()

    #adding data to dataset


    prodList = []
    setForCat = set()

    for key in obj:
        prodId = int(key[2:])
        prod=Product.objects.get(id=prodId)                 # product id
        cat = prod.category
        setForCat.add(cat)                                  # contain all unique category
        prodList.append(prod)

    for item in setForCat:
     rowUpdate = []
     rowUpdateCat = []
     for i in prodList:
            if i.category==item:
                rowUpdate.append(i.product_name.lower())            # list for row update
                rowUpdateCat.append(i.subCategory.lower())
            #          user ID, product ID, Seller ID, productName, productCategory, productSubCategory, productPrice,productDescription
            # updateList([user.id,i.id,i.seller,i.product_name.lower(),i.category.lower(),i.subCategory.lower(),i.price,i.desc.lower()],'OrderFullDetail.csv')          #UPDATING FULL DETAIL OF ORDER
     updateList(rowUpdate,'store_data1.csv')
     updateList(rowUpdateCat,'store_data1.csv')

     rowUpdate.insert(0,user.id)
     rowUpdateCat.insert(0,user.id)

     updateList(rowUpdate,'OrderDetail.csv')
     updateList(rowUpdateCat,'OrderDetail.csv')


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
def orderNotify(request,sellerId):
    seller = Seller.objects.get(id=sellerId)
    notificatons = OrderNotification.objects.filter(seller=seller)
    # print(notificatons)

    for i in notificatons:
        i.notificatonJson = json.loads(i.notificatonJson)
        print(i.notificatonJson)
    return render(request,"shop/orderNotify.html",{'notifications':notificatons})

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
