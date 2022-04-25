from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.pincodeInput, name='pincodeInput'),                              # (home page/landing page) of website
    path('pinResult/<int:result>', views.pinResult, name="pinResult"),              # if user is logged in
    path('cityResult/<str:stringResult>', views.cityResult, name="cityResult"),     # if user is logged in
    path('pincodeResult', views.pincodeResult, name="pincodeResult"),               # displaying result on the basis of input (unauthenticated user)
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handelLogin, name="handelLogin"),
    path('logout', views.handelLogout, name="handelLogout"),
    path("shopView/<int:shopid>", views.shopView, name="shopView"),
    path("productView/<int:prodid>", views.productView, name="productView"),
    path("cart/", views.cart, name="cart"),
    path("clearCart/", views.clearCart, name="clearCart"),
    path("checkout/", views.checkout, name="Checkout"),
    path("placeOrder/",views.placeOrder,name="placeOrder"),
    path("orderNotify/<int:sellerId>",views.orderNotify,name="orderNotify"),        # for Shop Owner
    path("tracker/",views.tracker,name="tracker"),
    path('newProduct/', views.newProduct, name="newProduct"),
    path('editProduct/<int:prodId>', views.editProduct, name="editProduct"),
    path('editProductHandle/', views.editProductHandle, name="editProductHandle"),
    path('deleteProduct/',views.deleteProduct, name="deleteProduct"),
    path('editShop/<int:sellId>', views.editShop, name="editShop"),
    path('editShopHandle/', views.editShopHandle, name="editShopHandle"),
    path("ratingPage/<int:id>/<str:val>",views.ratingPage,name="ratingPage"),
    path('shopRatingUpdate/', views.shopRatingUpdate, name="shopRatingUpdate"),
    path('prodRatingUpdate/', views.prodRatingUpdate, name="prodRatingUpdate"),
    path("exampleHomePage/",views.exampleHomePage,name="exampleHomePage"),
    path("search/",views.search,name="search"),
    path("searchResult/",views.searchResult,name="searchResult"),
    path("updateSearchFile/",views.updateSearchFile,name="updateSearchFile"),
    path("updateViews/",views.updateViews,name="updateViews"),
    path("updateCity/",views.updateCity,name="updateCity"),
    path("about/", views.about, name="about"),
    # path("<str:string>", views.error, name="error"),

]
