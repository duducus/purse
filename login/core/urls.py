# urls.py en la app core
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('exit/', views.exit, name='exit'),
    path('login/', LoginView.as_view(), name='login'), 
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('nuevo/', views.create_user, name='create_user'),
    path('usuarios/', views.users_list, name='users_list'), 
    path('informacion/', views.informacion, name='informacion'),
    path('pase-batalla/', views.pase_batalla, name='pase_batalla'),
    path('manage_points/', views.manage_points, name='manage_points'),
    path('movimientos_list/', views.movimientos_list, name='movimientos_list'), 
    path('generate_barcode/<int:user_id>/', views.generate_barcode, name='generate_barcode')
]
