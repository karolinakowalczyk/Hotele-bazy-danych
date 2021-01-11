from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from .models import Users, Rooms, Reservations
from .forms import SignUpForm, loginForm, BrowseForm
import datetime
from datetime import date, timedelta
import logging


currentUserId = 0

def index(request):
    user_list = Users.objects.order_by('surname')[:5]
    currentUserRole = "none"
    if(currentUserId!=0):
        currentUser = Users.objects.all().get(user_id=currentUserId)
        currentUserRole = currentUser.role

    context = {'user_list': user_list, 'user': currentUserId, 'userRole' : currentUserRole}
    return render(request, 'databaseapp/index.html', context)

def login(request):
    if request.method != 'POST':
        form = loginForm()
    else:
        form = loginForm(data = request.POST)
        users_list = Users.objects.order_by('user_id')
        if (users_list.filter(login=request.POST['login'], password=request.POST['password']).exists()): 
           currentUserLogin=request.POST['login']
           currentUser = Users.objects.all().get(login=currentUserLogin)
           global currentUserId
           currentUserId = currentUser.user_id
           currentUserRole = currentUser.role
           if currentUserRole == "admin" :
               return redirect('databaseapp:adminPanel')
           else:
               return redirect('databaseapp:userPanel')
        #nieudane logowanie - tymczasowo strona glowna
        else:
            return redirect('databaseapp:index')
    context = {'form': form}
    return render(request, 'databaseapp/login.html', context)

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
    if request.method != 'POST':
        form = BrowseForm()
    else:
        form = BrowseForm(data = request.POST)
        hotelId = request.POST['loc'][0]
        dateS = date(int(request.POST['dateS_year']),int(request.POST['dateS_month']),int(request.POST['dateS_day']))
        dateE = date(int(request.POST['dateE_year']),int(request.POST['dateE_month']),int(request.POST['dateE_day']))
        an = request.POST.get('animals', False)
        if form.is_valid():
            return browseResult(request, hotelId, dateS, dateE, an)
    today = date.today()
    rooms_list = Rooms.objects.order_by('room_id')
    rooms_list = rooms_list.filter(hotel=1)
    reservation_list = Reservations.objects.order_by('room')
    reservation_list = reservation_list.filter(date_start__lte=today, date_end__gte=today)
    context = {'rooms_list': rooms_list, 'reservation_list': reservation_list, 'form': form}
    return render(request, 'databaseapp/browse.html', context)

def browseResult(request, hotel_id, ds, de, an):
    reservation_list = Reservations.objects.order_by('room')
    reservation_list = conflictingReservations(reservation_list, ds, de)
    rooms_list = Rooms.objects.order_by('room_id')
    for res in reservation_list:
        rooms_list = rooms_list.exclude(room_id = res.room.room_id)
        print(res.room.room_id)
    if an:
        rooms_list = rooms_list.filter(hotel = hotel_id).exclude(animals=0)
    for r in rooms_list:
        print(r.room_id)
    context = {'rooms': rooms_list, 'date_start':ds, 'date_end':de, 'user':currentUserId}
    return render(request, 'databaseapp/browseresult.html', context)

def conflictingReservations(r, ds, de):
    a = r.filter(date_start__lte=ds, date_end__gte=de)
    b = r.filter(date_start__gte=ds, date_start__lte=de)
    c = r.filter(date_end__gte=ds, date_end__lte=de)
    d = a.union(b,c)
    return d

def userPanel(request):
    return render(request, 'databaseapp/userPanel.html')

def addReservation(request, room_id, date_start, date_end):
    ds = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    de = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    context = {'room_id':room_id, 'date_start':ds,'date_end':de}
    return render(request, 'databaseapp/addReservation.html', context)

def deleteReservation(request, reservation_id):
    context = {'reservation_id':reservation_id}
    return render(request, 'databaseapp/deleteReservation.html', context)

def deleteCurrentReservation(request, reservation_id):  
    reservationToDelete = Reservations.objects.get(reservation_id=reservation_id)
    reservationToDelete.delete()
    return redirect('databaseapp:showUserReservation')

def showUserReservation(request):
    deleteFailed = False
    reservation_list = Reservations.objects.order_by('reservation_id')
    reservation_list = reservation_list.filter(user = currentUserId)
    reservations_not_delete = reservation_list.filter(date_start__lte = (date.today() + timedelta(hours=48)))
    reservations_past = reservation_list.filter(date_end__lt = date.today())
    reservations_current = reservation_list.filter(date_start__gte = date.today())
    context = {'user':currentUserId, 'reservations' :reservation_list, 'reservations_not_delete' :reservations_not_delete, 'reservations_past' :reservations_past, 'reservations_current' :reservations_current}
    #context = {'user':currentUserId, 'reservations' :reservation_list}
    return render(request, 'databaseapp/showUserReservation.html', context)

def adminPanel(request):
    return render(request, 'databaseapp/adminPanel.html')

def signOut(request):
    global currentUserId
    currentUserId = 0
    return redirect('databaseapp:index')

def confirmReservation(request, room_id, date_start, date_end):
    ds = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    de = datetime.datetime.strptime(date_end, '%Y-%m-%d')
    res = Reservations(room=Rooms.objects.get(room_id=room_id), user=Users.objects.get(user_id=currentUserId), date_start=ds, date_end=de)
    res.save()
    return redirect('databaseapp:showUserReservation')

