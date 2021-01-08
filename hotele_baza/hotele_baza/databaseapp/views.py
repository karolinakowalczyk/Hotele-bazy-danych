from django.shortcuts import render

#from django.http import HttpResponse


def index(request):
    #return HttpResponse("Hello, world.")
    return render(request, 'databaseapp/index.html')
