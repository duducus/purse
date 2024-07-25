from django import forms
from .models import Venta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['usuario', 'descripcion', 'cantidad', 'precio_unitario', 'pago_efectivo', 'pago_puntos', 'pago_tarjeta']
        widgets = {
            'usuario': forms.Select(attrs={}),
            'descripcion': forms.TextInput(attrs={}),
            'cantidad': forms.NumberInput(attrs={}),
            'precio_unitario': forms.NumberInput(attrs={}),
            'pago_efectivo': forms.NumberInput(attrs={'value': 0}),
            'pago_puntos': forms.NumberInput(attrs={'value': 0}),
            'pago_tarjeta': forms.NumberInput(attrs={'value': 0}),
        }

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
