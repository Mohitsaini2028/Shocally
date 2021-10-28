from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.pincodeInput, name='pincodeInput'),                              # (home page/landing page) of website
    path('pinResult/<int:result>', views.pinResult, name="pinResult"),              # if user is logged in
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
    path("tracker/",views.tracker,name="tracker"),
    path('newProduct/', views.newProduct, name="newProduct"),
    path('editProduct/<int:prodId>', views.editProduct, name="editProduct"),
    path('editProductHandle/', views.editProductHandle, name="editProductHandle"),
    path('editShop/<int:sellId>', views.editShop, name="editShop"),
    path('editShopHandle/', views.editShopHandle, name="editShopHandle"),
    path("ratingPage/<int:id>/",views.ratingPage,name="ratingPage"),
    # path('RatingUpdate/', views.ShopRatingUpdate, name="ShopRatingUpdate"),
    path('prodRatingUpdate/', views.prodRatingUpdate, name="prodRatingUpdate"),

]
