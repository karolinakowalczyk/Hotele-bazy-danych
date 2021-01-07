from django.urls import path
from . import views

app_name = 'databaseapp'

urlpatterns = [
        path('', views.index, name='index')
    ]
