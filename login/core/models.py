from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_regalo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
