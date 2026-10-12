from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT, related_name="compras"
    )
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada_en"]

    def __str__(self):
        return f"Compra {self.pk}: {self.producto.nombre} x {self.cantidad}"
