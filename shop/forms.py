from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields="__all__"
