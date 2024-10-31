from django import forms
from .models import Torneo, InscripcionTorneo
from core.models import CustomUser
from django.utils import timezone

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'fecha_inicio', 'juego', 'lambda_value', 'comision']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'juego': forms.Select(choices=Torneo.JUEGOS_CHOICES, attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configura la fecha inicial como la fecha actual
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial']['fecha_inicio'] = timezone.now().date()


class InscripcionTorneoForm(forms.ModelForm):
    jugador_codigo = forms.CharField(label='Código del Jugador', max_length=12, widget=forms.TextInput())

    class Meta:
        model = InscripcionTorneo
        fields = ['jugador_codigo', 'entrada', 'posicion']
        widgets = {
            'entrada': forms.NumberInput(attrs={'required': True}),
            'posicion': forms.NumberInput(attrs={'required': True}),
        }

    def clean_jugador_codigo(self):
        codigo = self.cleaned_data.get('jugador_codigo')
        if codigo:
            try:
                jugador = CustomUser.objects.get(codigo=codigo)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("No se encontró ningún usuario con este código.")
            return jugador
        return None