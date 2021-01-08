from django.shortcuts import render
from .models import Users, Rooms

def index(request):
    user_list = Users.objects.order_by('surname')[:5]
    context = {'user_list': user_list}
    return render(request, 'databaseapp/index.html', context)

def login(request):
    return render(request, 'databaseapp/login.html')

def signUp(request):
    return render(request, 'databaseapp/signUp.html')

def browse(request):
    rooms_list = Rooms.objects.order_by('room_id')
    #rooms_list.filter()
    context = {'rooms_list': rooms_list}
    return render(request, 'databaseapp/browse.html', context)