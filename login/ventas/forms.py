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
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0','value': 0, 'oninput': "this.setCustomValidity('')", 'oninvalid': "this.setCustomValidity('No se permiten números negativos')"}),
            'pago_efectivo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': 0, 'oninput': "this.setCustomValidity('')", 'oninvalid': "this.setCustomValidity('No se permiten números negativos')"}),
            'pago_puntos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': 0, 'oninput': "this.setCustomValidity('')", 'oninvalid': "this.setCustomValidity('No se permiten números negativos')"}),
            'pago_tarjeta': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'value': 0, 'oninput': "this.setCustomValidity('')", 'oninvalid': "this.setCustomValidity('No se permiten números negativos')"}),
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
        
        if precio_unitario < 0:
            self.add_error('precio_unitario', "No se permiten números negativos.")
        if pago_efectivo < 0:
            self.add_error('pago_efectivo', "No se permiten números negativos.")
        if pago_puntos < 0:
            self.add_error('pago_puntos', "No se permiten números negativos.")
        if pago_tarjeta < 0:
            self.add_error('pago_tarjeta', "No se permiten números negativos.")
        
        if total_pagado > precio_total:
            raise forms.ValidationError("Exceso de pago")

        if total_pagado < precio_total:
            raise forms.ValidationError("El total pagado no coincide con el precio total")
        


        return cleaned_data
