from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Torneo, InscripcionTorneo
from .forms import TorneoForm, InscripcionTorneoForm
from django.forms import modelformset_factory

@login_required
def lista_torneos(request):
    torneos = Torneo.objects.all()
    return render(request, 'torneos/lista_torneos.html', {'torneos': torneos})

@login_required
def torneo_detail(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    inscripciones = torneo.inscripciones_torneo.all()

    if request.method == 'POST':
        form = InscripcionTorneoForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.torneo = torneo
            inscripcion.save()
            return redirect('torneo_detail', pk=torneo.pk)
    else:
        form = InscripcionTorneoForm()

    return render(request, 'torneos/detalle_torneo.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
        'form': form,
    })

@login_required
def crear_torneo(request):
    InscripcionFormSet = modelformset_factory(InscripcionTorneo, form=InscripcionTorneoForm, extra=1)
    if request.method == 'POST':
        torneo_form = TorneoForm(request.POST)
        inscripcion_formset = InscripcionFormSet(request.POST, queryset=InscripcionTorneo.objects.none())
        if torneo_form.is_valid() and inscripcion_formset.is_valid():
            torneo = torneo_form.save()
            for form in inscripcion_formset:
                inscripcion = form.save(commit=False)
                inscripcion.torneo = torneo
                inscripcion.save()
            return redirect('torneo_list')
        else:
            print(torneo_form.errors)  # Para depurar errores de validación
            print(inscripcion_formset.errors)  # Para depurar errores de validación
    else:
        torneo_form = TorneoForm()
        inscripcion_formset = InscripcionFormSet(queryset=InscripcionTorneo.objects.none())

    return render(request, 'torneos/crear_torneo.html', {
        'torneo_form': torneo_form,
        'inscripcion_formset': inscripcion_formset,
    })