from django.db import models
from core.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

class Venta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ventas')
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    pago_efectivo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pago_puntos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pago_tarjeta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.precio_total = self.precio_unitario * Decimal(self.cantidad)
        super().save(*args, **kwargs)

    def total_pagado(self):
        total = (self.pago_efectivo or 0) + (self.pago_puntos or 0) + (self.pago_tarjeta or 0)
        return total

    def pago_correcto(self):
        return self.total_pagado() == self.precio_total

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} - {self.fecha}"

@receiver(post_save, sender=Venta)
def actualizar_saldo_usuario(sender, instance, created, **kwargs):
    if created:
        usuario = instance.usuario
        porcentaje = Decimal('0.03')  # 3% en formato decimal
        monto_a_sumar = instance.precio_total * porcentaje
        usuario.saldo += monto_a_sumar
        usuario.save()

@receiver(post_delete, sender=Venta)
def restar_saldo_usuario(sender, instance, **kwargs):
    usuario = instance.usuario
    porcentaje = Decimal('0.03')  # 3% en formato decimal
    monto_a_restar = instance.precio_total * porcentaje
    usuario.saldo -= monto_a_restar
    usuario.save()