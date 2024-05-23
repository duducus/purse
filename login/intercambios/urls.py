# intercambios/urls.py
from django.urls import path
from .views import lista_intercambios, nuevo_intercambio

urlpatterns = [
    path('', lista_intercambios, name='lista_intercambios'),
    path('nuevo/', nuevo_intercambio, name='nuevo_intercambio'),
]
