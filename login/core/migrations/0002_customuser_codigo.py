# Generated by Django 5.0.6 on 2024-05-24 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='codigo',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
