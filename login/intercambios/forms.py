# intercambios/forms.py
from django import forms
from .models import Intercambio

class IntercambioForm(forms.ModelForm):
    class Meta:
        model = Intercambio
        fields = ['monto']

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        intercambio = super().save(commit=False)
        if self.usuario:
            intercambio.usuario = self.usuario
        if commit:
            intercambio.save()
        return intercambio
