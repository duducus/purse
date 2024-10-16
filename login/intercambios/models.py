from django.db import models
from core.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import logging
logger = logging.getLogger('django')


class Intercambio(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    articulo = models.CharField(max_length=255, default='artículo')
    fecha = models.DateTimeField(auto_now_add=True)  # Agregamos el campo de fecha

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Verificamos si el monto es negativo y actuamos en consecuencia
        if self.monto < 0:
            monto_a_restar = abs(self.monto)  # Convertir monto a positivo
            if self.usuario.saldo_regalo > 0:
                if self.usuario.saldo_regalo >= monto_a_restar:
                    # Si saldo_regalo es suficiente para cubrir todo el monto
                    self.usuario.saldo_regalo -= monto_a_restar
                else:
                    # Si saldo_regalo no es suficiente, restamos lo que se pueda y el resto del saldo
                    monto_a_restar -= self.usuario.saldo_regalo
                    self.usuario.saldo_regalo = 0
                    self.usuario.saldo -= monto_a_restar  # Restamos lo que queda al saldo normal
            else:
                # Si no hay saldo_regalo, restamos directamente del saldo
                self.usuario.saldo -= monto_a_restar
        else:
            # Si el monto es positivo, sumamos al saldo
            self.usuario.saldo += self.monto

        logger.debug(f"Saldo regalo después de guardar: {self.usuario.saldo_regalo}")
        logger.debug(f"Saldo después de guardar: {self.usuario.saldo}")
        self.usuario.save()
