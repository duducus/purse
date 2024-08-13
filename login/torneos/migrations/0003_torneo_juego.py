# Generated by Django 5.0.6 on 2024-08-09 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneos', '0002_remove_torneo_jugadores_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='juego',
            field=models.CharField(choices=[('yu_gi_oh', 'Yu Gi Oh'), ('magic', 'Magic'), ('pokemon', 'Pokémon'), ('heroclix', 'Heroclix')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]