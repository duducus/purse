# Generated by Django 5.0.8 on 2024-10-31 00:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0004_torneo_comision_torneo_lambda_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torneo',
            name='fecha_inicio',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
