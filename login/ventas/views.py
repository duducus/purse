from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Venta
from .forms import VentaForm
from django.http import JsonResponse
from core.models import CustomUser
from django.shortcuts import get_object_or_404
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def lista_todas_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/lista_todas_ventas.html', {'ventas': ventas})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def agregar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        codigo_usuario = request.POST.get('codigo_usuario')  # Capturamos el código del POST
        if form.is_valid():
            venta = form.save(commit=False)
            
            # Intentamos buscar el usuario por su código
            try:
                usuario = CustomUser.objects.get(codigo=codigo_usuario)
                venta.usuario = usuario  # Asignamos el usuario a la venta
                
                # Usar el saldo de regalo
                pago_puntos = int(request.POST.get('pago_puntos', 0))  # Obtén el valor ingresado de puntos
                if pago_puntos > usuario.saldo_regalo:
                    form.add_error('pago_puntos', 'No puedes usar más puntos de los disponibles.')
                else:
                    usuario.saldo_regalo -= pago_puntos  # Descontamos del saldo de regalo
                    usuario.save()  # Guardamos el usuario con el nuevo saldo

            except CustomUser.DoesNotExist:
                form.add_error('usuario', 'Usuario no encontrado con ese código')  # Agregamos error al form
            
            venta.save()
            return redirect('lista_todas_ventas')
    else:
        form = VentaForm()
    
    return render(request, 'ventas/agregar_venta.html', {'form': form})


def buscar_usuario(request, codigo):
    usuario = get_object_or_404(CustomUser, codigo=codigo)
    return JsonResponse({
        'usuario_encontrado': True,
        'saldo_regalo': usuario.saldo_regalo,
    })
