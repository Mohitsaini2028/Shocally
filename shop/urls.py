from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.pincodeInput, name='pincodeInput'),
    path('pinResult', views.pinResult, name='pinResult'),
]
