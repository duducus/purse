from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Venta
from .forms import VentaForm
from django.http import JsonResponse
from core.models import CustomUser
from django.shortcuts import get_object_or_404
from django.urls import reverse
from decimal import Decimal

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def lista_todas_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista_todas_ventas.html', {'ventas': ventas})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def agregar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        codigo_usuario = request.POST.get('codigo_usuario')

        # Obtenemos el valor de pago_puntos y lo convertimos en Decimal
        pago_puntos = request.POST.get('pago_puntos', 0)
        try:
            pago_puntos = Decimal(pago_puntos)
        except (ValueError, TypeError):
            form.add_error('pago_puntos', 'Ingresa un valor numérico válido para los puntos.')

        if form.is_valid():
            venta = form.save(commit=False)
            
            try:
                usuario = CustomUser.objects.get(codigo=codigo_usuario)
                venta.usuario = usuario
                
                total_saldo_disponible = usuario.saldo + usuario.saldo_regalo
                if pago_puntos > total_saldo_disponible:
                    form.add_error('pago_puntos', 'No puedes usar más puntos de los disponibles.')
                else:
                    # Restamos del saldo_regalo primero, luego del saldo normal
                    if pago_puntos <= usuario.saldo_regalo:
                        usuario.saldo_regalo -= pago_puntos
                    else:
                        puntos_restantes = pago_puntos - usuario.saldo_regalo
                        usuario.saldo_regalo = 0
                        usuario.saldo -= puntos_restantes

                    usuario.save()

            except CustomUser.DoesNotExist:
                form.add_error('usuario', 'Usuario no encontrado con ese código')

            venta.save()

            # Redirige a la lista de usuarios con el código en la URL
            return redirect(f'/usuarios/search/?codigo={codigo_usuario}')

    else:
        form = VentaForm()

    return render(request, 'ventas/agregar_venta.html', {'form': form})


# Función para buscar usuario y traer ambos saldos: saldo y saldo_regalo
def buscar_usuario(request, codigo):
    usuario = get_object_or_404(CustomUser, codigo=codigo)
    return JsonResponse({
        'usuario_encontrado': True,
        'saldo_regalo': usuario.saldo_regalo,
        'saldo': usuario.saldo,  # Traer también el saldo normal del usuario
    })
