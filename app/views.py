from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import json
import requests

# Create your views here.
url = 'http://127.0.0.1:5000/'

def inicio(request):
    if request.method == 'POST':
        
        if 'entrada' in request.POST:
            entrada = request.POST['entrada']

            objeto = {
                'archivo': entrada
            }
            r = requests.post(url+'entrada', json=objeto, verify=True)
            
        if 'file' in request.POST:
            file = request.POST['file']
            print(file)
        if 'archivo' in request.POST:
            file = request.POST['archivo']
            print(file)

        
    return render(request, 'app/base.html')

def login(request):
    return HttpResponse("Login")