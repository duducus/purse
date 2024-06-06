import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_regalo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    codigo = models.CharField(max_length=12, blank=True, unique=True, null=True)  # Agregar campo "código"

@receiver(post_save, sender=CustomUser)
def agregar_codigo_a_usuario(sender, instance, created, **kwargs):
    if created and not instance.codigo:  # Solo ejecutar si el usuario se está creando por primera vez y no tiene un código
        while True:
            nuevo_codigo = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            if not CustomUser.objects.filter(codigo=nuevo_codigo).exists():  # Verificar si el código es único
                instance.codigo = nuevo_codigo
                instance.save()
                break
