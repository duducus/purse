# Generated by Django 5.0.6 on 2024-06-25 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_customuser_puntos_pase_pkm'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='puntos_pase_magic',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='puntos_pase_yugioh',
            field=models.IntegerField(default=0),
        ),
    ]
