from django import forms
from .models import Venta
from core.models import CustomUser

class VentaForm(forms.ModelForm):
    usuario_codigo = forms.CharField(label='Código del Usuario', max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Venta
        fields = ['usuario_codigo', 'descripcion', 'cantidad', 'precio_unitario', 'pago_efectivo', 'pago_puntos', 'pago_tarjeta']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'pago_efectivo': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
            'pago_puntos': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
            'pago_tarjeta': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
        }

    def clean_usuario_codigo(self):
        codigo = self.cleaned_data.get('usuario_codigo')
        if codigo:
            try:
                usuario = CustomUser.objects.get(codigo=codigo)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("No se encontró ningún usuario con este código.")
            return usuario
        return None

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad', 0)
        precio_unitario = cleaned_data.get('precio_unitario', 0)
        precio_total = cantidad * precio_unitario

        pago_efectivo = cleaned_data.get('pago_efectivo', 0) or 0
        pago_puntos = cleaned_data.get('pago_puntos', 0) or 0
        pago_tarjeta = cleaned_data.get('pago_tarjeta', 0) or 0
        total_pagado = pago_efectivo + pago_puntos + pago_tarjeta

        if total_pagado > precio_total:
            raise forms.ValidationError("Exceso de pago")

        if total_pagado < precio_total:
            raise forms.ValidationError("El total pagado no coincide con el precio total")

        return cleaned_data
