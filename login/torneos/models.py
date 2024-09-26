from django.conf import settings
from django.db import models
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP
import math
from django.db import transaction

class Torneo(models.Model):
    JUEGOS_CHOICES = [
        ('yu_gi_oh', 'Yu Gi Oh'),
        ('magic', 'Magic'),
        ('pokemon', 'Pokémon'),
        ('heroclix', 'Heroclix'),
    ]

    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    juego = models.CharField(max_length=20, choices=JUEGOS_CHOICES)
    lambda_value = models.DecimalField(max_digits=5, decimal_places=3, default=0.3)
    comision = models.DecimalField(max_digits=4, decimal_places=2, default=0.15)

    def __str__(self):
        return self.nombre

class InscripcionTorneo(models.Model):
    torneo = models.ForeignKey('Torneo', related_name='inscripciones_torneo', on_delete=models.CASCADE)
    jugador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entrada = models.DecimalField(max_digits=10, decimal_places=2)
    posicion = models.PositiveIntegerField()
    premio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def factor_x(self):
        lambda_value = self.torneo.lambda_value
        total_entradas = Decimal(self.torneo.inscripciones_torneo.aggregate(total_entradas=models.Sum('entrada'))['total_entradas'] or 0)
        total_participantes = Decimal(self.torneo.inscripciones_torneo.count() or 1)
        
        if self.posicion is None:
            return Decimal('0.000000')
        
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
        comision = self.torneo.comision
        total_entradas = Decimal(self.torneo.inscripciones_torneo.aggregate(total_entradas=models.Sum('entrada'))['total_entradas'] or 0)
        
        if total_entradas == 0:
            return Decimal('0.00')

        premio_calculado_value = (self.porcentaje * total_entradas * (1 - comision)) / Decimal('100')
        premio_calculado_value = premio_calculado_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        premio_calculado_value = premio_calculado_value.quantize(Decimal('1'), rounding=ROUND_UP)
        return premio_calculado_value

    def save(self, *args, **kwargs):
        self.premio = self.premio_calculado
        with transaction.atomic():
            super().save(*args, **kwargs)
            
            # Lógica para ajustar el saldo y saldo_regalo
            premio = self.premio_calculado
            jugador = self.jugador

            if premio > 0:
                # Primero verificamos si el saldo es negativo
                if jugador.saldo < 0:
                    # Calculamos cuánto se necesita para llevar el saldo a 0
                    deficit = abs(jugador.saldo)

                    if premio >= deficit:
                        # Si el premio es mayor o igual al déficit, llevamos el saldo a 0
                        jugador.saldo = 0
                        # Lo que sobra se suma a saldo_regalo
                        jugador.saldo_regalo += (premio - deficit)
                    else:
                        # Si el premio no cubre todo el déficit, simplemente sumamos al saldo
                        jugador.saldo += premio
                else:
                    # Si el saldo es 0 o mayor, sumamos directamente a saldo_regalo
                    jugador.saldo_regalo += premio

                # Guardamos los cambios del jugador
                jugador.save()