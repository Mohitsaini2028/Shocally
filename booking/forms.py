from django import forms

class NewBookingItemForm(forms.Form):
    service_name = forms.CharField()
    category = forms.CharField()
    subCategory = forms.CharField()
    originalPrice = forms.FloatField()
    price = forms.FloatField()
    desc = forms.CharField(widget=forms.Textarea)
    img = forms.ImageField()

class NewTimeSlotForm(forms.Form):
    starting_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    ending_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    max_booking = forms.IntegerField()             #how many person can book at that time/slot
    bookingDate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
