from django.shortcuts import render, HttpResponse ,HttpResponseRedirect
from .models import User, Seller, BookingItem, Booking, TimeSlot, BookingUpdate, BookingItemRating
from math import ceil
from booking.forms import NewBookingItemForm, NewTimeSlotForm
from django.contrib.auth.decorators import login_required
import time
# Create your views here.

def home(request):
    # pinCode=458441
    pinCode = 452001
    print("BOOKING HOME PAGE USER PINCODE",request.POST.get('code'))
    allShop=[]
    prod=[]
    catprods = Seller.objects.values('shopCategory', 'id')
    cats = {item['shopCategory'] for item in catprods}
    print("\n\n\n\n\n",catprods,"- - - - ",cats)
    nSlides = ''
    for cat in cats:
        # prod=User.objects.filter(PINCODE=pinCode,is_Seller=True,Category=cat)
        shop=Seller.objects.filter(pincode=pinCode,shopCategory=cat,appointmentBased=True)
        if shop.exists():
            n = len(shop)

            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allShop.append([shop, range(1, nSlides), nSlides])



    print(allShop)
    params = {'allShop':allShop,'nSlides':nSlides}

    return render(request, 'booking/bookingPage.html', params)


# def shopView(request,shopid):
#     shop= Seller.objects.filter(id=shopid)
#     # Products=Product.objects.filter(seller=shop)
#     allProds = []
#     EXIST=[]
#
#     catprods = Product.objects.values('category', 'id')
#     cats = {item['category'] for item in catprods}
#
#     for cat in cats:
#         # prod = Product.objects.filter(seller=shop[0],category=cat)
#         prod = Product.objects.filter(seller=shop[0],category=cat)
#         if prod.exists():
#             n = len(prod)
#             nSlides = n // 4 + ceil((n / 4) - (n // 4))
#             allProds.append([prod, range(1, nSlides), nSlides])
#     print(allProds)
#     if len(allProds)==0:
#         prodExist=False
#         prodExist=True
#
#     form = NewProductForm()
#
#     return render(request, 'shopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist ,'form':form} )


def timeSlot(request,shopid):
    shop= Seller.objects.filter(id=shopid)
    timeSlot = TimeSlot.objects.filter(seller=shopid)

    slotForm = NewTimeSlotForm()
    return render(request, 'booking/timeSlot.html', {'shop':shop[0],'timeSlot':timeSlot, 'slotForm':slotForm} )

def shopView(request,shopid):
    shop= Seller.objects.filter(id=shopid)
    # Products=Product.objects.filter(seller=shop)
    timeSlot = TimeSlot.objects.filter(seller=shopid)
    allProds = []
    EXIST=[]

    catprods = BookingItem.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        # prod = Product.objects.filter(seller=shop[0],category=cat)
        prod = BookingItem.objects.filter(seller=shop[0],category=cat)
        if prod.exists():
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    print(allProds)
    if len(allProds)==0:
        prodExist=False
    else:
        prodExist=True

    form = NewBookingItemForm()
    slotForm = NewTimeSlotForm()

    return render(request, 'booking/bookingShopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist ,'form':form, 'slotForm':slotForm} )
    #return render(request, 'booking/bookingShopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist, 'timeSlot':timeSlot} )


def bookingItemView(request,itemid):
    bookingItem = BookingItem.objects.filter(id=itemid)
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
    return render(request, 'booking/bookingItemView.html', {'bookingItem':bookingItem[0]})

def appointmentBook(request):
    bookingItem = BookingItem.objects.get(id=request.POST['bookingItemId'])
    timeSlot = TimeSlot.objects.get(id=request.POST['bookingSlotId'])

    if request.POST['bookingSlotId'] == "":
            messages.error(request,"please add Time Slot for your booking. ")
    else:
        timeSlot.max_booking-=1
        booking=Booking.objects.create(user=request.user, item=bookingItem, time=timeSlot)
        descripton = f"The Booking is Confirmed for {bookingItem.service_name} at {timeSlot.starting_time} - {timeSlot.ending_time} - Date {timeSlot.bookingDate} "
        update = BookingUpdate(booking_id=booking, update_desc=descripton)
        booking.save()
        update.save()
        timeSlot.save()

    return HttpResponseRedirect(f"/booking/ShopView/{bookingItem.seller.id}")

def appointmentNotify(request,sellerId):
    seller = Seller.objects.get(id=sellerId)
    notificatons = Booking.objects.filter(item__seller=seller)
    # print(notificatons)

    for i in notificatons:
        print(i)
    return render(request,"booking/appointmentNotify.html",{'notifications':notificatons})


def update(request):
    bookings=Booking.objects.filter(user=request.user)
    bookingUpdate=[]

    for booking in bookings:
        print("\n\n- - - - - - - ",booking)
        update=BookingUpdate.objects.filter(booking_id=booking.id)
        if update:
            bookingUpdate.append(update)
            print("\n\n - - - - - - - Update Page- - - - - - - - \n\n")
    print(bookings,bookingUpdate)
    return render(request,'booking/update.html',{'bookings':bookings,'bookingUpdate':bookingUpdate})

def ItemBookPage(request,itemId):
    item = BookingItem.objects.get(id=itemId)
    # seller = Seller.objects.filter(id=item.seller.id)
    timeSlot = TimeSlot.objects.filter(seller=item.seller)
    return render(request,'booking/itemBookingPage.html',{'item':item, 'timeSlot':timeSlot})


def NewBookingItem(request):
    if request.method=='POST':
        form=NewBookingItemForm(request.POST)
        bookingItem= BookingItem()
        bookingItem.service_name=form.data['service_name']
        bookingItem.category=form.data['category']
        bookingItem.subCategory=form.data['subCategory']
        bookingItem.originalPrice=form.data['originalPrice']
        bookingItem.price=form.data['price']
        bookingItem.desc=form.data['desc']
        bookingItem.image=request.FILES.get('img')

        seller=Seller.objects.get(id=request.POST['sellerId'])
        bookingItem.seller=seller
        bookingItem.save()
        return HttpResponseRedirect(f"/booking/ShopView/{request.POST['sellerId']}")

def NewTimeSlot(request):
    if request.method=='POST':
        form=NewTimeSlotForm(request.POST)
        timeslot= TimeSlot()
        timeslot.starting_time=form.data['starting_time']
        timeslot.ending_time=form.data['ending_time']
        timeslot.max_booking=form.data['max_booking']
        timeslot.bookingDate=form.data['bookingDate']

        seller=Seller.objects.get(id=request.POST['sellerId'])
        timeslot.seller=seller
        timeslot.save()
        return HttpResponseRedirect(f"/booking/timeSlot/{request.POST['sellerId']}")


@login_required(login_url='/')
def editBookingItem(request,bookId):
    bookingItem=BookingItem.objects.get(id=bookId)
    fields={'service_name':bookingItem.service_name, 'category':bookingItem.category,'subCategory':bookingItem.subCategory,'originalPrice':bookingItem.originalPrice,'price':bookingItem.price,'desc':bookingItem.desc,'img':bookingItem.image}
    form=NewBookingItemForm(initial=fields)
    return  render(request, "booking/editBookingItem.html",{'form':form,'bookingItem':bookingItem})

@login_required(login_url='/')
def editBookingItemHandle(request):
    if request.method=="POST":
        form=NewBookingItemForm(request.POST)
        bookingItem=BookingItem()
        oldbookingItem=BookingItem.objects.get(id=request.POST['ItemId'])
        bookingItem.id=oldbookingItem.id
        bookingItem.service_name=form.data['service_name']
        bookingItem.category=form.data['category']
        bookingItem.subCategory=form.data['subCategory']
        bookingItem.originalPrice=form.data['originalPrice']
        bookingItem.price=form.data['price']
        bookingItem.desc=form.data['desc']

        if request.FILES.get('img'):
            bookingItem.image=request.FILES.get('img')
        else:
            bookingItem.image=oldbookingItem.image
        seller=Seller.objects.get(id=request.POST['sellerId'])
        bookingItem.seller=seller
        bookingItem.save()
    return HttpResponseRedirect(f"/booking/ShopView/{request.POST['sellerId']}")

@login_required(login_url='/')
def deleteBookingItem(request):
    bookingItemId=int(request.POST['delProd'])
    sellerId=int(request.POST['sellerId'])

    bookingItem=BookingItem.objects.get(id=bookingItemId)
    bookingItem.delete()
    messages.success(request, "Service is successfully deleted")
    return HttpResponseRedirect(f"/booking/ShopView/{sellerId}")


@login_required(login_url='/')
def bookingItemRatingUpdate(request):
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

def bookingItemRatingUpdate(request):
    id=request.user.id

    bookingItem=BookingItem.objects.get(id=request.POST['Id'])
    number=float(request.POST['RatingGiven'])
    print(type(number))
    print("\n\n\n\n")
    print("before",bookingItem.rating,bookingItem.ratingNo)
    bookingItem.ratingNo+=1
    bookingItem.rating = (bookingItem.rating*(bookingItem.ratingNo-1) + number)/bookingItem.ratingNo
    print("after",bookingItem.rating)
    time.sleep(2.4)

    bookingItem.save()
    try:
        bookingItemUpdate = BookingItemRating.objects.get(user=request.user,product=prod)
        #if user already rated the same product
        print("bookingItemUpdate",bookingItemUpdate)
        bookingItemUpdate.rating=number
        bookingItemUpdate.comment=request.POST['comment']
        bookingItemUpdate.save()
        print(" Already Rated")
    except Exception as e:
        print("Exception Rating Page",e)
        # if first time rating
        bookingItemRat=BookingItemRating.objects.create(user=request.user,bookingItem=bookingItem,rating=number,comment=request.POST['comment'])
        bookingItemRat.save()
        print(" First Time Rated")

    return HttpResponseRedirect(f"/booking/bookingItemView/{request.POST['Id']}")
