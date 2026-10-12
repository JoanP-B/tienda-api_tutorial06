from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from .models import Compra, Producto


@transaction.atomic
def comprar_producto(producto_id: int, cantidad: int) -> Compra:
    try:
        producto = Producto.objects.select_for_update().get(pk=producto_id)
    except Producto.DoesNotExist as exc:
        raise NotFound("El producto solicitado no existe.") from exc

    if producto.stock < cantidad:
        raise ValidationError(
            {"cantidad": "No hay existencias suficientes para completar la compra."}
        )

    producto.stock -= cantidad
    producto.save(update_fields=["stock"])
    total = producto.precio * Decimal(cantidad)
    return Compra.objects.create(
        producto=producto,
        cantidad=cantidad,
        total=total,
    )
