from django import forms
from .models import Users, Locations, Hotels, Reservations
from datetime import date

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password','email', 'phone', 'name', 'surname']
        labels = {'login': 'login', 'password': 'password', 'email': 'email', 'phone': 'phone', 'name': 'name', 'surname': 'surname'}
        widgets = {
            'password': forms.PasswordInput,
            'email': forms.EmailInput,
        }

class loginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password']
        labels = {'login': 'login', 'password': 'password'}
        widgets = {
            'password': forms.PasswordInput,
        }

class BrowseForm(forms.Form):
    LOCATIONS=[]
    for h in Hotels.objects.all().prefetch_related('location'):
        loc = ""+h.location.city+", "+h.location.street+" "+str(h.location.number)
        LOCATIONS.append((h.hotel_id,loc))
    loc = forms.CharField(label='test:', widget=forms.Select(choices=LOCATIONS))
    dateS = forms.DateField(label='dateStart', widget=forms.SelectDateWidget(years=range(date.today().year,date.today().year+4)))
    dateE = forms.DateField(label='dateEnd', widget=forms.SelectDateWidget(years=range(date.today().year,date.today().year+4)))
