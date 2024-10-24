# Generated by Django 5.0.6 on 2024-06-06 14:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torneo',
            name='jugadores',
        ),
        migrations.AlterField(
            model_name='inscripciontorneo',
            name='jugador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inscripciontorneo',
            name='posicion',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='inscripciontorneo',
            name='premio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
