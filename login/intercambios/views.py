from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Intercambio
from .forms import IntercambioForm
import logging

logger = logging.getLogger(__name__)

@login_required
def lista_intercambios(request):
    intercambios = Intercambio.objects.filter(usuario=request.user)
    return render(request, 'intercambios/lista_intercambios.html', {'intercambios': intercambios})

@login_required
def nuevo_intercambio(request):
    if request.method == 'POST':
            form = IntercambioForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('lista_todos_intercambios')  # Redirige a la lista de intercambios después de guardar
    else:
        form = IntercambioForm()
    return render(request, 'intercambios/nuevo_intercambio.html', {'form': form})

#def es_staff(user):
#   return user.is_staff

#@user_passes_test(es_staff)
@login_required
def lista_todos_intercambios(request):
    intercambios = Intercambio.objects.all()
    return render(request, 'intercambios/lista_todos_intercambios.html', {'intercambios': intercambios})
