from django import forms
from .models import Torneo, InscripcionTorneo

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'fecha_inicio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class InscripcionTorneoForm(forms.ModelForm):
    class Meta:
        model = InscripcionTorneo
        fields = ['jugador', 'entrada', 'posicion']
        widgets = {
            'jugador': forms.Select(attrs={'class': 'form-control'}),
            'entrada': forms.NumberInput(attrs={'class': 'form-control'}),
            'posicion': forms.NumberInput(attrs={'class': 'form-control'}),
        }
