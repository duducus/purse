from django import forms
from .models import Venta
from core.models import CustomUser

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['usuario', 'descripcion', 'cantidad', 'precio_unitario', 'pago_efectivo', 'pago_puntos', 'pago_tarjeta']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'pago_efectivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'pago_puntos': forms.NumberInput(attrs={'class': 'form-control'}),
            'pago_tarjeta': forms.NumberInput(attrs={'class': 'form-control'}),
        }