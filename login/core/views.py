# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from torneos.models import InscripcionTorneo
from intercambios.models import Intercambio

@login_required
def home(request):
    saldo = 0
    saldo_regalo = 0
    torneos_usuario = []  # Lista para almacenar los detalles de los torneos del usuario
    intercambios_usuario = []  # Lista para almacenar los detalles de los intercambios del usuario
    
    if request.user.is_authenticated:
        saldo = request.user.saldo
        saldo_regalo = request.user.saldo_regalo
        
        # Filtrar los torneos en los que el usuario está inscrito
        inscripciones = InscripcionTorneo.objects.filter(jugador=request.user)
        for inscripcion in inscripciones:
            torneos_usuario.append({
                'nombre': inscripcion.torneo.nombre,
                'entrada': inscripcion.entrada,
                'premio': inscripcion.premio,
                'posicion': inscripcion.posicion
            })

        # Filtrar los intercambios del usuario
        intercambios = Intercambio.objects.filter(usuario=request.user)
        for intercambio in intercambios:
            intercambios_usuario.append({
                'articulo': intercambio.articulo,
                'monto': intercambio.monto
            })

    return render(request, 'core/home.html', {
        'saldo': saldo,
        'saldo_regalo': saldo_regalo,
        'torneos_usuario': torneos_usuario,
        'intercambios_usuario': intercambios_usuario
    })

def products(request):
    user_authenticated = request.user.is_authenticated
    context = {'user_authenticated': user_authenticated}
    if user_authenticated:
        # Agrega cualquier dato específico para usuarios autenticados aquí
        pass
    return render(request, 'core/products.html', context)

def exit(request):
    logout(request)
    return redirect('home')
