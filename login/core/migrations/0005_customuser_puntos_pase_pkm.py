# Generated by Django 5.0.6 on 2024-06-13 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_customuser_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='puntos_pase_pkm',
            field=models.IntegerField(default=0),
        ),
    ]
