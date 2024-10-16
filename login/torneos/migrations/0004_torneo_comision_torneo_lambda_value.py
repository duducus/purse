# Generated by Django 5.0.6 on 2024-08-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0003_torneo_juego'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='comision',
            field=models.DecimalField(decimal_places=2, default=0.15, max_digits=4),
        ),
        migrations.AddField(
            model_name='torneo',
            name='lambda_value',
            field=models.DecimalField(decimal_places=3, default=0.3, max_digits=5),
        ),
    ]
