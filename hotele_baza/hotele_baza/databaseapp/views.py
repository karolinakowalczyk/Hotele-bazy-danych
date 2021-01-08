from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from .models import Users, Rooms, Reservations
from .forms import SignUpForm
from datetime import date


def index(request):
    user_list = Users.objects.order_by('surname')[:5]
    context = {'user_list': user_list}
    return render(request, 'databaseapp/index.html', context)

def login(request):
    return render(request, 'databaseapp/login.html')

def signUp(request):
    if request.method != 'POST':
        form = SignUpForm()
    else:
        form = SignUpForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('databaseapp:index')
    context = {'form': form}
    return render(request, 'databaseapp/signUp.html', context)

def browse(request):
    today = date.today()
    rooms_list = Rooms.objects.order_by('room_id')
    rooms_list = rooms_list.filter(hotel=2)
    reservation_list = Reservations.objects.order_by('room')
    reservation_list = reservation_list.filter(date_start__lte=today, date_end__gte=today)
    
    context = {'rooms_list': rooms_list, 'reservation_list': reservation_list}
    return render(request, 'databaseapp/browse.html', context)