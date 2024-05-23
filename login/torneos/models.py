from django.db import models
from core.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    jugadores = models.ManyToManyField(CustomUser, through='InscripcionTorneo', related_name='torneos_torneo')

    def __str__(self):
        return self.nombre

class InscripcionTorneo(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='inscripciones_torneo')
    jugador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='torneos_inscripciones')
    entrada = models.DecimalField(max_digits=10, decimal_places=2)
    premio = models.DecimalField(max_digits=10, decimal_places=2)
    posicion = models.IntegerField()

    def __str__(self):
        return f"{self.jugador} - {self.torneo}"

@receiver(post_save, sender=InscripcionTorneo)
def agregar_premio_a_saldo_regalo(sender, instance, created, **kwargs):
    if created:
        jugador = instance.jugador
        jugador.saldo_regalo += instance.premio
        jugador.save()

@receiver(post_delete, sender=InscripcionTorneo)
def restar_premio_de_saldo_regalo(sender, instance, **kwargs):
    jugador = instance.jugador
    jugador.saldo_regalo -= instance.premio
    jugador.save()
