from django.db import models
from decimal import Decimal
from Apps.rutas.models import Ruta
class Cliente(models.Model):

    nombre = models.CharField(max_length=256)
    direccion = models.TextField(max_length=256, blank=False, null=False)
    telefono = models.CharField(max_length=30, blank=False, null=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=False, null=True)
    activo = models.BooleanField(default=True, blank=False, null=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'clientes'
    
    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'saldo': self.saldo,
        }