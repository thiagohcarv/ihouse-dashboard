# Generated by Django 2.1.4 on 2018-12-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_auto_20181213_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='finish_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora de Finalização'),
        ),
    ]