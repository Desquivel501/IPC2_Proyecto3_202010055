from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def inicio(request):
    if request.method == 'POST':
        if 'entrada' in request.POST:
            entrada = request.POST['entrada']
            print("Entrada: ", entrada)
        if 'file' in request.POST:
            file = request.POST['file']
            print(file)
    return render(request, 'app/base.html')

def login(request):
    return HttpResponse("Login")