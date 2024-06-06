# intercambios/admin.py
from django.contrib import admin
from .models import Intercambio


@admin.register(Intercambio)
class IntercambioAdmin(admin.ModelAdmin):
    list_display = ('monto', 'usuario','articulo')
    search_fields = ['usuario__username']
