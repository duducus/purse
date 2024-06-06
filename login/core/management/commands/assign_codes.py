# core/management/commands/assign_codes.py
from django.core.management.base import BaseCommand
from core.models import CustomUser
import random

class Command(BaseCommand):
    help = 'Assign unique codes to users without one'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        for user in users:
            if not user.codigo:
                while True:
                    nuevo_codigo = ''.join([str(random.randint(0, 9)) for _ in range(12)])
                    if not CustomUser.objects.filter(codigo=nuevo_codigo).exists():
                        user.codigo = nuevo_codigo
                        user.save()
                        break
            else:
                # Check if the current code is unique
                while CustomUser.objects.filter(codigo=user.codigo).count() > 1:
                    nuevo_codigo = ''.join([str(random.randint(0, 9)) for _ in range(12)])
                    if not CustomUser.objects.filter(codigo=nuevo_codigo).exists():
                        user.codigo = nuevo_codigo
                        user.save()
                        break
        self.stdout.write(self.style.SUCCESS('Successfully assigned or ensured unique codes for all users'))
