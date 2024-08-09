from django.contrib import admin
from .models import Torneo, InscripcionTorneo

class InscripcionTorneoInline(admin.TabularInline):
    model = InscripcionTorneo
    extra = 1

class TorneoAdmin(admin.ModelAdmin):
    inlines = [InscripcionTorneoInline]
    list_display = ('nombre', 'fecha_inicio','juego')
    search_fields = ('nombre',)

admin.site.register(Torneo, TorneoAdmin)
