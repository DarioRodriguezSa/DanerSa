# Generated by Django 3.2.6 on 2023-12-30 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_rename_idprducto_producto_idproducto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='existencia',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
