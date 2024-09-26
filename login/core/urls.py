# urls.py en la app core
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('generate_barcode/<int:user_id>/', views.generate_barcode, name='generate_barcode'),
    path('usuarios/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('usuarios/search/', views.search_users, name='search_users'),
     path('buscar_usuario/', views.buscar_usuario, name='buscar_usuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)