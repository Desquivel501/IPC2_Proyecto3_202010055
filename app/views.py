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

def graph(request):
    return render(request, 'app/graph.html')

def graphIva(request):
    return render(request, 'app/graphIVA2.html')

def graphFecha(request):
    return render(request, 'app/graphFechas.html')


def getTablaIva(request):
    if request.method == 'POST':
        print("GET!")
        
        post_data = json.loads(request.body.decode("utf-8"))
        
        nit = post_data['nit']
        desde = post_data['desde']
        hasta = post_data['hasta']
        
        desde_list = desde.split("-")
        desde_list = desde_list[::-1]
        desde = str(desde_list[0]+"/"+desde_list[1]+"/"+desde_list[2])
        
        hasta_list = hasta.split("-")
        hasta_list = hasta_list[::-1]
        hasta = str(hasta_list[0]+"/"+hasta_list[1]+"/"+hasta_list[2])

        objeto = {
            "nit":nit,
            "desde":desde,
            "hasta":hasta
        }

        requests_response = requests.post(url+'getTablaIva', json=objeto, verify=True)
        
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )

    return HttpResponse(django_response)

def getTablaFechas(request):
    if request.method == 'POST':
        print("GET!")
        
        post_data = json.loads(request.body.decode("utf-8"))
        
        iva = post_data['iva']
        desde = post_data['desde']
        hasta = post_data['hasta']
        
        desde_list = desde.split("-")
        desde_list = desde_list[::-1]
        desde = str(desde_list[0]+"/"+desde_list[1]+"/"+desde_list[2])
        
        hasta_list = hasta.split("-")
        hasta_list = hasta_list[::-1]
        hasta = str(hasta_list[0]+"/"+hasta_list[1]+"/"+hasta_list[2])
  
        objeto = {
            "iva":iva,
            "desde":desde,
            "hasta":hasta
        }
        
        requests_response = requests.post(url+'getTablaFecha', json=objeto, verify=True)
        
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )

    return HttpResponse(django_response)


def reset(request):
    if request.method == 'GET':
        print("GET!")
        requests_response  = requests.get(url+'reset', verify=True)
        
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )

    return HttpResponse(django_response)



def getTablaIva2(request):
    if request.method == 'POST':
        print("GET!")
        
        post_data = json.loads(request.body.decode("utf-8"))
        
        fecha = post_data['fecha']
        
        desde_list = fecha.split("-")
        desde_list = desde_list[::-1]
        fecha = str(desde_list[0]+"/"+desde_list[1]+"/"+desde_list[2])
        

        objeto = {
            "fecha":fecha
        }

        requests_response = requests.post(url+'getTablaIva', json=objeto, verify=True)
        
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )

    return HttpResponse(django_response)


def getSalidaPDF(request):
    if request.method == 'GET':
        print("GET!")
        requests_response  = requests.get(url+'salidaPDF', verify=True)
        
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )

    return HttpResponse(django_response)