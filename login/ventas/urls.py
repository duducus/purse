from django.urls import path
from . import views

urlpatterns = [
    path('todos-ventas/', views.lista_todas_ventas, name='lista_todas_ventas'),
    # otras rutas...
]
