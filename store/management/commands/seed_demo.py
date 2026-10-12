from django.core.management.base import BaseCommand

from store.models import Producto


class Command(BaseCommand):
    help = "Crea productos de demostración si todavía no existen."

    def handle(self, *args, **options):
        productos = [
            ("Café EAFIT", "Café molido de origen colombiano.", "18000.00", 20),
            ("Termo universitario", "Termo reutilizable de 500 ml.", "32000.00", 10),
            ("Cuaderno de arquitectura", "Cuaderno de 100 hojas.", "12000.00", 30),
        ]
        for nombre, descripcion, precio, stock in productos:
            _, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "precio": precio,
                    "stock": stock,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Creado: {nombre}"))
            else:
                self.stdout.write(f"Ya existe: {nombre}")
