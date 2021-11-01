from django import forms

class NewBookingItemForm(forms.Form):
    service_name = forms.CharField()
    category = forms.CharField()
    subCategory = forms.CharField()
    originalPrice = forms.FloatField()
    price = forms.FloatField()
    desc = forms.CharField(widget=forms.Textarea)
    img = forms.ImageField()
