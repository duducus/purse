# urls.py en la app core
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('exit/', views.exit, name='exit'),
    path('login/', LoginView.as_view(), name='login'),  # Utiliza la vista de inicio de sesión predeterminada de Django
    # Otras URLs...
]
