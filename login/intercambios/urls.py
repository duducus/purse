# intercambios/urls.py
from django.urls import path
from .views import lista_intercambios, nuevo_intercambio
from . import views

urlpatterns = [
    path('lista/', lista_intercambios, name='lista_intercambios'),
    path('nuevo/', nuevo_intercambio, name='nuevo_intercambio'),
    path('', views.lista_todos_intercambios, name='lista_todos_intercambios'),
    
]
