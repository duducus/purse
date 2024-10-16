from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
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
            return redirect('lista_todos_intercambios')
        else:
            messages.error(request, 'Código de usuario no encontrado')
    else:
        form = IntercambioForm()
    return render(request, 'intercambios/nuevo_intercambio.html', {'form': form})

@login_required
def lista_todos_intercambios(request):
    intercambios = Intercambio.objects.all()
    return render(request, 'intercambios/lista_todos_intercambios.html', {'intercambios': intercambios})
