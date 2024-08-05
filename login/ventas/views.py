from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Venta
from .forms import VentaForm

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
        if form.is_valid():
            venta = form.save(commit=False)
            usuario = form.cleaned_data.get('usuario_codigo')
            if usuario:
                venta.usuario = usuario
            venta.save()
            return redirect('lista_todas_ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/agregar_venta.html', {'form': form})
