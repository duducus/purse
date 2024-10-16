from django.contrib import admin
from .models import Venta

class VentaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descripcion', 'cantidad', 'precio_unitario', 'precio_total', 'fecha','pago_efectivo','pago_puntos','pago_tarjeta')
    search_fields = ('usuario__username', 'descripcion')

admin.site.register(Venta, VentaAdmin)
