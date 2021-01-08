from django.shortcuts import render
from .models import Users



def index(request):
    user_list = Users.objects.order_by('surname')[:5]
    context = {'user_list': user_list}
    return render(request, 'databaseapp/index.html', context)
