from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path('', inicio),
    path('login', login),
    path('getSalida', getSalida),
]
