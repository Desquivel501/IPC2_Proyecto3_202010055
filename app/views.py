from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
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

    return render(request, 'app/base.html')

def getSalida(request):
    if request.method == 'GET':
        print("GET!")
        requests_response  = requests.get(url+'getSalida', verify=True)
        
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )

    return HttpResponse(django_response)
        
def login(request):
    return HttpResponse("Login")