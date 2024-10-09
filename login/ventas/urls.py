from django.urls import path
from . import views

urlpatterns = [
    path('todos-ventas/', views.lista_todas_ventas, name='lista_todas_ventas'),
    path('nueva-venta/', views.agregar_venta, name='agregar_venta'),
    path('buscar_usuario/<str:codigo>/', views.buscar_usuario, name='buscar_usuario'),
    # otras rutas...
]
