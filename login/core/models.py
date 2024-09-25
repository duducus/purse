import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from torneos.models import Torneo, InscripcionTorneo

class CustomUser(AbstractUser):
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_regalo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    codigo = models.CharField(max_length=12, blank=True, unique=True, null=True)
    puntos_pase_pkm = models.IntegerField(default=0)
    puntos_pase_yugioh = models.IntegerField(default=0)
    puntos_pase_magic = models.IntegerField(default=0)
    puntos_pase_heroclix = models.IntegerField(default=0) 
    telefono = models.CharField(max_length=10, blank=True, null=True) 
    apellidos = models.CharField(max_length=255, blank=True, null=True) 
    foto = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.puntos_pase_pkm < 0:
            self.puntos_pase_pkm = 0
        if self.puntos_pase_yugioh < 0:
            self.puntos_pase_yugioh = 0
        if self.puntos_pase_magic < 0:
            self.puntos_pase_magic = 0
        if self.puntos_pase_heroclix < 0:
            self.puntos_pase_heroclix = 0 
        super().save(*args, **kwargs)

class Movimiento(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    puntos_pokemon = models.IntegerField()
    puntos_yugioh = models.IntegerField()
    puntos_magic = models.IntegerField()
    puntos_heroclix = models.IntegerField(default=0)  # Nuevo campo
    concepto = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.user.username} - {self.concepto}'

@receiver(post_save, sender=CustomUser)
def agregar_codigo_a_usuario(sender, instance, created, **kwargs):
    if created and not instance.codigo:  # Solo ejecutar si el usuario se está creando por primera vez y no tiene un código
        while True:
            nuevo_codigo = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            if not CustomUser.objects.filter(codigo=nuevo_codigo).exists():  # Verificar si el código es único
                instance.codigo = nuevo_codigo
                instance.save()
                break
