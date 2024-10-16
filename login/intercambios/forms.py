# intercambios/forms.py
from django import forms
from .models import Intercambio
from core.models import CustomUser

class IntercambioForm(forms.ModelForm):
    codigo_usuario = forms.CharField(label='Código del Usuario', max_length=12)

    class Meta:
        model = Intercambio
        fields = ['codigo_usuario', 'monto', 'articulo']

    def clean_codigo_usuario(self):
        codigo = self.cleaned_data.get('codigo_usuario')
        try:
            usuario = CustomUser.objects.get(codigo=codigo)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('Usuario no encontrado')
        return usuario

    def save(self, commit=True):
        intercambio = super().save(commit=False)
        intercambio.usuario = self.cleaned_data['codigo_usuario']
        if commit:
            intercambio.save()
        return intercambio
