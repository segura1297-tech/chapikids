from django.db import models
from catalogo.models import Producto
from catalogo.validators import validar_telefono_mexicano, validar_fecha_futura, validar_precio_positivo


class Pedido(models.Model):
    """Pedido de piñatas con estados y detalle de líneas."""
    ESTADOS = [
        ('nuevo', 'Nuevo'),
        ('confirmado', 'Confirmado'),
        ('preparacion', 'En preparación'),
        ('entregado', 'Entregado/Cerrado'),
        ('cancelado', 'Cancelado'),
    ]

    folio = models.CharField(max_length=20, unique=True, editable=False)
    cliente_nombre = models.CharField(max_length=200)
    cliente_telefono = models.CharField(max_length=20, validators=[validar_telefono_mexicano])
    cliente_email = models.EmailField(blank=True)
    fecha_evento = models.DateField(validators=[validar_fecha_futura])
    notas = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='nuevo'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-creado']

    def __str__(self):
        return f'Pedido {self.folio} - {self.cliente_nombre}'

    def save(self, *args, **kwargs):
        if self.folio:
            super().save(*args, **kwargs)
            return

        # El folio se armaba con "el ultimo folio + 1". Si dos cotizaciones
        # entran al mismo tiempo, las dos leen el mismo ultimo folio,
        # generan el mismo numero y la segunda revienta con IntegrityError
        # por la restriccion UNIQUE. Se reintenta unas cuantas veces: en la
        # practica nunca hace falta mas de uno.
        from datetime import datetime

        from django.db import IntegrityError, transaction

        for intento in range(5):
            year = datetime.now().year
            ultimo = Pedido.objects.filter(
                folio__startswith=f'PED-{year}'
            ).order_by('folio').last()

            numero = int(ultimo.folio.split('-')[-1]) + 1 if ultimo else 1
            self.folio = f'PED-{year}-{numero:04d}'

            try:
                with transaction.atomic():
                    super().save(*args, **kwargs)
                return
            except IntegrityError:
                # Otro pedido secontro este folio al mismo tiempo: se
                # descarta el save y se vuelve a calcular.
                if intento == 4:
                    raise


class PedidoItem(models.Model):
    """Línea de pedido (producto + cantidad)."""
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'

    def __str__(self):
        return f'{self.cantidad}x {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
