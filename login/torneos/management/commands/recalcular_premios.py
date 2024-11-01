from django.core.management.base import BaseCommand
from torneos.models import InscripcionTorneo

class Command(BaseCommand):
    help = 'Recalcula los premios de todas las inscripciones de torneos existentes.'

    def handle(self, *args, **kwargs):
        inscripciones = InscripcionTorneo.objects.all()
        for inscripcion in inscripciones:
            # Recalcula el premio y actualiza el saldo del jugador
            inscripcion.premio = inscripcion.premio_calculado
            inscripcion.save()
            self.stdout.write(f'Se recalculó el premio para {inscripcion.jugador} en el torneo {inscripcion.torneo.nombre}.')

        self.stdout.write(self.style.SUCCESS('Todos los premios han sido recalculados con éxito.'))
