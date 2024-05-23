from django import forms
from .models import Player

class TorneoForm(forms.Form):
    num_jugadores = forms.IntegerField(min_value=1, max_value=10)

    def save_jugadores(self):
        num_jugadores = self.cleaned_data['num_jugadores']
        for i in range(1, num_jugadores + 1):
            self.fields[f'nombre_{i}'] = forms.CharField(label=f'Nombre del Jugador {i}')
            self.fields[f'entrada_{i}'] = forms.DecimalField(label=f'Entrada del Jugador {i}')
            self.fields[f'posicion_{i}'] = forms.ChoiceField(label=f'Posición del Jugador {i}', choices=Jugador.POSICIONES)
            self.fields[f'premio_{i}'] = forms.DecimalField(label=f'Premio del Jugador {i}')

    def crear_jugadores(self):
        num_jugadores = self.cleaned_data['num_jugadores']
        for i in range(1, num_jugadores + 1):
            nombre = self.cleaned_data[f'nombre_{i}']
            entrada = self.cleaned_data[f'entrada_{i}']
            posicion = self.cleaned_data[f'posicion_{i}']
            premio = self.cleaned_data[f'premio_{i}']
            Jugador.objects.create(nombre=nombre, entrada=entrada, posicion=posicion, premio=premio)
