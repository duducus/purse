# Generated by Django 5.0.8 on 2024-10-19 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_customuser_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='correo_arena',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='konami_ID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pop_ID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]