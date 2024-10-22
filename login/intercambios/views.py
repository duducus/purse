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
            # Guarda el intercambio
            intercambio = form.save()
            
            # Obtiene el código del usuario al que se hizo el intercambio
            codigo_usuario = form.cleaned_data.get('codigo_usuario')  # Asegúrate de que este sea el nombre correcto del campo en tu formulario
            print(codigo_usuario)
            # Redirige a la URL de búsqueda con el código del usuario
            return redirect(f'/usuarios/search/?codigo={codigo_usuario}')
        else:
            messages.error(request, 'Código de usuario no encontrado')
    else:
        form = IntercambioForm()
    return render(request, 'intercambios/nuevo_intercambio.html', {'form': form})

@login_required
def lista_todos_intercambios(request):
    intercambios = Intercambio.objects.all()
    return render(request, 'intercambios/lista_todos_intercambios.html', {'intercambios': intercambios})
