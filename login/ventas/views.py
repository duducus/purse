from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Venta

#def es_staff(user):
 #   return user.is_staff

@login_required
#@user_passes_test(es_staff)
def lista_todas_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/lista_todas_ventas.html', {'ventas': ventas})
