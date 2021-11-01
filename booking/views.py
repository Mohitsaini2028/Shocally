from django.shortcuts import render, HttpResponse ,HttpResponseRedirect
from .models import User, Seller, BookingItem, Booking, TimeSlot, BookingUpdate, BookingItemRating
from math import ceil
from booking.forms import NewBookingItemForm
import time
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    pinCode=458441
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
#     # BookingItems=BookingItem.objects.filter(seller=shop)
#     allProds = []
#     EXIST=[]
#
#     catprods = BookingItem.objects.values('category', 'id')
#     cats = {item['category'] for item in catprods}
#
#     for cat in cats:
#         # prod = BookingItem.objects.filter(seller=shop[0],category=cat)
#         prod = BookingItem.objects.filter(seller=shop[0],category=cat)
#         if prod.exists():
#             n = len(prod)
#             nSlides = n // 4 + ceil((n / 4) - (n // 4))
#             allProds.append([prod, range(1, nSlides), nSlides])
#     print(allProds)
#     if len(allProds)==0:
#         prodExist=False
#         prodExist=True
#
#     form = NewBookingItemForm()
#
#     return render(request, 'shopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist ,'form':form} )


def shopView(request,shopid):
    shop= Seller.objects.filter(id=shopid)
    # BookingItems=BookingItem.objects.filter(seller=shop)
    timeSlot = TimeSlot.objects.filter(seller=shopid)
    allProds = []
    EXIST=[]

    catprods = BookingItem.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        # prod = BookingItem.objects.filter(seller=shop[0],category=cat)
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

    return render(request, 'booking/bookingShopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist ,'form':form} )
    #return render(request, 'booking/bookingShopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist, 'timeSlot':timeSlot} )


def bookingItemView(request,itemid):
    bookingItem = BookingItem.objects.filter(id=itemid)
    # recommendations = BookingItem.objects.filter(category=BookingItem[0].category).order_by('-rating')
    # print(recommendations)
    recommendations = []

    # count = 0
    # for  i in BookingItem.objects.filter(category=BookingItem[0].category,subCategory=BookingItem[0].subCategory).order_by('-rating'):
    #     if i.seller.Pincode == BookingItem[0].seller.Pincode:
    #             recommendations.append(i)
    #     if count>=5:
    #         break
    #     count+=1
    # seller.PinCode=BookingItem[0].seller.Pincode,

    # a=clusterRecommend.run(BookingItem[0].subCategory)
    # print(a)
    # suggestions = []
    # try:
    #     suggestions = aprori_recommender.run(BookingItem[0].subCategory)
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
        bookingItemUpdate = BookingItemRating.objects.get(user=request.user,BookingItem=prod)
        #if user already rated the same BookingItem
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

@login_required(login_url='/')
def editBookingItem(request,itemId):
    bookingItem=BookingItem.objects.get(id=itemId)
    fields={'service_name':bookingItem.service_name, 'category':bookingItem.category,'subCategory':bookingItem.subCategory,'originalPrice':bookingItem.originalPrice,'price':bookingItem.price,'desc':bookingItem.desc,'img':bookingItem.image }
    form=NewBookingItemForm(initial=fields)
    return  render(request, "booking/editBookingItem.html",{'form':form,'bookingItem':bookingItem})

@login_required(login_url='/')
def editBookingItemHandle(request):
    if request.method=="POST":
        form=NewBookingItemForm(request.POST)
        bookingItem=BookingItem()
        oldBookingItem=BookingItem.objects.get(id=request.POST['ItemId'])
        bookingItem.id=oldBookingItem.id
        bookingItem.service_name=form.data['service_name']
        bookingItem.category=form.data['category']
        bookingItem.subCategory=form.data['subCategory']
        bookingItem.originalPrice=form.data['originalPrice']
        bookingItem.price=form.data['price']
        bookingItem.desc=form.data['desc']
        if request.FILES.get('img'):
            bookingItem.image=request.FILES.get('img')
        else:
            bookingItem.image=oldBookingItem.image
        seller=Seller.objects.get(id=request.POST['sellerId'])
        bookingItem.seller=seller
        bookingItem.save()
    return HttpResponseRedirect(f"/booking/ShopView/{request.POST['sellerId']}")
