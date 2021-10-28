from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path('', inicio),
    path('login', login),
    path('getSalida', getSalida),
    path('graphs', graph),
    path('graphs-iva', graphIva),
    path('graphs-fechas', graphFecha),
    path('getTablaIva', getTablaIva),
    path('getTablaFechas', getTablaFechas),
    path('reset', reset),
]
