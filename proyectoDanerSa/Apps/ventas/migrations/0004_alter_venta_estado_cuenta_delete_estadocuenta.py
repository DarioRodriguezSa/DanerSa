# Generated by Django 4.1.5 on 2024-01-19 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_remove_estadocuenta_pagada_estadocuenta_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='estado_cuenta',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='EstadoCuenta',
        ),
    ]
