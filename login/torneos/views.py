from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Torneo, InscripcionTorneo
from .forms import TorneoForm, InscripcionTorneoForm
from django.forms import modelformset_factory
from core.models import CustomUser
from django.http import JsonResponse
from django.utils import timezone

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def lista_torneos(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    return render(request, 'torneos/lista_torneos.html', {'torneos': torneos})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def torneo_detail(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    inscripciones = torneo.inscripciones_torneo.all()

    total_entradas = sum(inscripcion.entrada for inscripcion in inscripciones)
    total_premios = sum(inscripcion.premio_calculado for inscripcion in inscripciones)
    ganancias_torneos = total_entradas - total_premios

    if request.method == 'POST':
        form = InscripcionTorneoForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            jugador = form.cleaned_data.get('jugador_codigo')
            if jugador:
                inscripcion.jugador = jugador
            inscripcion.torneo = torneo
            inscripcion.save()
            return redirect('torneo_detail', pk=torneo.pk)
    else:
        form = InscripcionTorneoForm()

    return render(request, 'torneos/detalle_torneo.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
        'form': form,
        'ganancias_torneos': ganancias_torneos,
    })

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def crear_torneo(request):
    InscripcionFormSet = modelformset_factory(InscripcionTorneo, form=InscripcionTorneoForm, extra=1)
    
    if request.method == 'POST':
        torneo_form = TorneoForm(request.POST)
        inscripcion_formset = InscripcionFormSet(request.POST, queryset=InscripcionTorneo.objects.none())
        
        if torneo_form.is_valid() and inscripcion_formset.is_valid():
            torneo = torneo_form.save()
            for form in inscripcion_formset:
                if form.is_valid():
                    inscripcion = form.save(commit=False)
                    jugador = form.cleaned_data.get('jugador_codigo')
                    if jugador:
                        inscripcion.jugador = jugador
                    inscripcion.torneo = torneo
                    inscripcion.save()
                    
                    # Actualizar los puntos del pase de batalla
                    juego = torneo.juego
                    puntos_a_sumar = 10
                    if juego == 'pokemon':
                        inscripcion.jugador.puntos_pase_pkm += puntos_a_sumar
                    elif juego == 'yu_gi_oh':
                        inscripcion.jugador.puntos_pase_yugioh += puntos_a_sumar
                    elif juego == 'magic':
                        inscripcion.jugador.puntos_pase_magic += puntos_a_sumar
                    elif juego == 'heroclix':
                        inscripcion.jugador.puntos_pase_heroclix += puntos_a_sumar
                    inscripcion.jugador.save()

            # Calcula los premios y actualiza los saldos
            actualizar_saldos(torneo)
            
            return redirect('torneo_list')
        else:
            print(torneo_form.errors)
            print(inscripcion_formset.errors)
    
    else:
        fecha_actual = timezone.now().date().strftime('%Y-%m-%d')
        torneo_form = TorneoForm(initial={'fecha_inicio': fecha_actual})
        inscripcion_formset = InscripcionFormSet(queryset=InscripcionTorneo.objects.none())

    return render(request, 'torneos/crear_torneo.html', {
        'torneo_form': torneo_form,
        'inscripcion_formset': inscripcion_formset,
    })


def search_users_torneo(request):
    codigo = request.GET.get('codigo')
    usuario_nombre = None

    if codigo:
        try:
            usuarios = CustomUser.objects.filter(codigo=codigo)
            if usuarios.exists():
                usuario = usuarios.first()
                usuario_nombre = usuario.username
            else:
                usuario_nombre = 'Usuario no encontrado'
        except ValueError:
            usuario_nombre = 'Código no válido'
    else:
        usuario_nombre = 'Ingrese un código'

    return render(request, 'torneos/create_torneo.html', {'usuario_nombre': usuario_nombre})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def eliminar_torneo(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    if request.method == 'POST':
        torneo.delete()
        return redirect('torneo_list')
    return render(request, 'torneos/eliminar_torneo.html', {'torneo': torneo})

def actualizar_saldos(torneo):
    inscripciones = torneo.inscripciones_torneo.all()
    for inscripcion in inscripciones:
        # Calcula el premio
        inscripcion.premio = inscripcion.premio_calculado
        inscripcion.save()

        jugador = inscripcion.jugador
        premio = inscripcion.premio

        if premio > 0:
            # Ajusta los saldos como se indicó previamente
            if jugador.saldo < 0:
                deficit = abs(jugador.saldo)
                if premio >= deficit:
                    jugador.saldo = 0
                    jugador.saldo_regalo += (premio - deficit)
                else:
                    jugador.saldo += premio
            else:
                jugador.saldo_regalo += premio
            jugador.save()
