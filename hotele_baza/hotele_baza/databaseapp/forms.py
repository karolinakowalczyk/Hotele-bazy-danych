from django import forms
from django.core.exceptions import ValidationError
from .models import Users, Locations, Hotels, Reservations
from datetime import date
import re


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password','email', 'phone', 'name', 'surname']
        labels = {'login': 'login', 'password': 'password', 'email': 'email', 'phone': 'phone', 'name': 'name', 'surname': 'surname'}
        widgets = {
            'password': forms.PasswordInput,
            'email': forms.EmailInput,
        }

    def clean(self):
        login = self.cleaned_data['login']
        pwd = self.cleaned_data['password']
        phone = self.cleaned_data['phone']
        name = self.cleaned_data['name']
        sur = self.cleaned_data['surname']

        if re.search('[^-a-zA-Z0-9_!#$%&\'*+,./:;<=>?@]', login):
            self.add_error('login',"Login can only contain: letters, numbers and the following special characters: -_!#$%&\'*+,./:;<=>?@")
        if re.search('[^-a-zA-Z0-9_!#$%&\'*+,./:;<=>?@]', pwd):
            self.add_error('password',"Password can only contain: letters, numbers and the following special characters: -_!#$%&\'*+,./:;<=>?@")
        elif not bool(re.match('[a-zA-Z]+[0-9]+',pwd)):
            self.add_error('password',"Password needs to contain at least one letter and one number")
        if phone:
            if re.search('[^-0-9\+]', phone):
                self.add_error('phone',"Incorrect phone format - only numbers, - and + allowed")
        if re.search('[^-a-zA-Z\' ]', name):
            self.add_error('name',"Incorrect name format - only letters, spaces, - and ' allowed")
        if re.search('[^-a-zA-Z\' ]', sur):
            self.add_error('surname',"Incorrect name format - only letters, spaces, - and ' allowed")


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
    loc = forms.CharField(label='Hotel:', widget=forms.Select(choices=LOCATIONS))
    dateS = forms.DateField(label='Start date: ', widget=forms.SelectDateWidget(years=range(date.today().year,date.today().year+4)))
    dateE = forms.DateField(label='End date: ', widget=forms.SelectDateWidget(years=range(date.today().year,date.today().year+4)))
    animals = forms.BooleanField(label='Require animals: ', required=False)

    def clean(self):
        cleaned_data = super().clean()
        ds = cleaned_data.get("dateS")
        de = cleaned_data.get("dateE")

        if de < date.today():
            self.add_error('dateE',"The dates cannot be in the past")
        if ds < date.today():
            self.add_error('dateS',"The dates cannot be in the past")
        if ds > de:
            self.add_error('dateE','Start date must be before end date')

class HotelsForm(forms.Form):
    LOCATIONS=[]
    for h in Hotels.objects.all().prefetch_related('location'):
        loc = ""+h.location.city+", "+h.location.street+" "+str(h.location.number)
        LOCATIONS.append((h.hotel_id,loc))
    loc = forms.CharField(widget=forms.Select(choices=LOCATIONS))

class PwdForm(forms.Form):
    old = forms.CharField(label='Old password:', widget=forms.PasswordInput)
    new = forms.CharField(label='New password:', widget=forms.PasswordInput)

    def clean(self):
        old = self.cleaned_data['old']
        new = self.cleaned_data['new']

        if re.search('[^-a-zA-Z0-9_!#$%&\'*+,./:;<=>?@]', new):
            self.add_error('new',"Password can only contain: letters, numbers and the following special characters: -_!#$%&\'*+,./:;<=>?@")
        elif not bool(re.match('[a-zA-Z]+[0-9]+',new)):
            self.add_error('new',"Password needs to contain at least one letter and one number")
        if old == new:
            self.add_error('new',"New password must be different from the old one")
            self.add_error('old',"")
      