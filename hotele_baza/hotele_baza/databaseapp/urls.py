from django.urls import path
from . import views

app_name = 'databaseapp'

urlpatterns = [
        path('', views.index, name='index'),
        path('login/', views.login, name='login'),
        path('signUp/', views.signUp, name='signUp'),
        path('browse/', views.browse, name='browse'),
        path('userPanel/', views.userPanel, name='userPanel')
    ]
