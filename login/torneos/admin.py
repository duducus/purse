from django.contrib import admin
from .models import Torneo, InscripcionTorneo

class InscripcionTorneoInline(admin.TabularInline):
    model = InscripcionTorneo
    extra = 0
    readonly_fields = ('premio_calculado',)  # Mostrar el cálculo en lugar del premio guardado
    exclude = ('premio',)
    
    def premio_calculado(self, instance):
        return instance.premio_calculado  # Uso directo de la propiedad para consistencia

class TorneoAdmin(admin.ModelAdmin):
    inlines = [InscripcionTorneoInline]
    list_display = ('nombre', 'fecha_inicio','juego')
    search_fields = ('nombre',)

admin.site.register(Torneo, TorneoAdmin)
