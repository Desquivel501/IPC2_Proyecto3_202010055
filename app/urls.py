from django.urls import path, include
from .views import signin, home

urlpatterns = [
    path('', home, name='home'),
    path('signin', signin, name='signin'),
]
