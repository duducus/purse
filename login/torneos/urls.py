# urls.py
from django.urls import path
from .views import lista_torneos, torneo_detail, crear_torneo

urlpatterns = [
    path('', lista_torneos, name='torneo_list'),
    path('<int:pk>/', torneo_detail, name='torneo_detail'),
    path('nuevo/', crear_torneo, name='crear_torneo'),
]
