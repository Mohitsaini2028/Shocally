from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.pincodeInput, name='pincodeInput'),
    path('pinResult', views.pinResult, name='pinResult'),
    path('signup', views.handleSignUp, name="handleSignUp"),
    # path('login', views.handelLogin, name="handelLogin"),
    # path('logout', views.handelLogout, name="handelLogout"),

]
