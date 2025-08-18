from django.http import HttpResponse
from django.shortcuts import render

#def index(request):
    #return HttpResponse("Hello World")

def showDemoPage(request):
    return render (request, "demo.html")