# Generated by Django 5.0.6 on 2024-08-09 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_customuser_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='apellidos',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]