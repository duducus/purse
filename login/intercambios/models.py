from django.db import models
from core.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Intercambio(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    articulo = models.CharField(max_length=255, default='artículo')
    fecha = models.DateTimeField(auto_now_add=True)  # Agregamos el campo de fecha

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.usuario.saldo_regalo += self.monto
        self.usuario.save()

@receiver(post_delete, sender=Intercambio)
def restar_intercambio_de_saldo(sender, instance, **kwargs):
    usuario = instance.usuario
    usuario.saldo -= instance.monto
    usuario.save()
