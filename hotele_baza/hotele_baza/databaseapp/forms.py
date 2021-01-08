from django import forms
from .models import Users

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
