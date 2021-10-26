from django.shortcuts import render, HttpResponse ,HttpResponseRedirect
from .models import User, Seller, BookingItem, Booking, TimeSlot
from math import ceil
from booking.forms import NewBookingItemForm
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

    return render(request, 'booking/bookingShopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist ,'form':form} )
    #return render(request, 'booking/bookingShopView.html', {'shop':shop[0],'allProds':allProds,'prodExist':prodExist, 'timeSlot':timeSlot} )

def appointmentBook(request):
    pass

def ItemBookPage(request,itemId):
    item = BookingItem.objects.get(id=itemId)
    # seller = Seller.objects.filter(id=item.seller.id)
    timeSlot = TimeSlot.objects.filter(seller=item.seller)
    return render(request,'ItemBookingPage.html',{'item':item, 'timeSlot':timeSlot})


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
