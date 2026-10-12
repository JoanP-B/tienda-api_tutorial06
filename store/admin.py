from django.contrib import admin

from .models import Compra, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "stock")
    search_fields = ("nombre",)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "cantidad", "total", "creada_en")
    list_filter = ("creada_en",)
