from django.conf import settings
from django.db import models
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP
import math

class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()

class InscripcionTorneo(models.Model):
    torneo = models.ForeignKey('Torneo', related_name='inscripciones_torneo', on_delete=models.CASCADE)
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entrada = models.DecimalField(max_digits=10, decimal_places=2)
    posicion = models.PositiveIntegerField()
    premio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def factor_x(self):
        lambda_value = Decimal(0.3)
        total_entradas = Decimal(self.torneo.inscripciones_torneo.aggregate(total_entradas=models.Sum('entrada'))['total_entradas'] or 0)
        total_participantes = Decimal(self.torneo.inscripciones_torneo.count() or 1)
        probabilidad = Decimal(math.exp(-lambda_value * self.posicion))
        
        if total_entradas == 0 or total_participantes == 0:
            return Decimal('0.000000')

        factor_x_value = probabilidad * (Decimal(self.entrada) / (total_entradas / total_participantes))
        return factor_x_value.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)

    @property
    def porcentaje(self):
        total_factor_x = sum([inscripcion.factor_x for inscripcion in self.torneo.inscripciones_torneo.all()]) or Decimal('1')
        porcentaje_value = (self.factor_x / total_factor_x) * Decimal('100')
        return porcentaje_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def premio_calculado(self):
        comision = Decimal(0.15)
        total_entradas = Decimal(self.torneo.inscripciones_torneo.aggregate(total_entradas=models.Sum('entrada'))['total_entradas'] or 0)
        
        if total_entradas == 0:
            return Decimal('0.00')

        premio_calculado_value = (self.porcentaje * total_entradas * (1 - comision)) / Decimal('100')
        premio_calculado_value = premio_calculado_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        premio_calculado_value = premio_calculado_value.quantize(Decimal('1'), rounding=ROUND_UP)
        return premio_calculado_value

    def save(self, *args, **kwargs):
        self.premio = self.premio_calculado
        super().save(*args, **kwargs)