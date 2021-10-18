from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def inicio(request):
    return HttpResponse("Ejemplo")

def login(request):
    return HttpResponse("Login")