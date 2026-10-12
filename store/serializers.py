from rest_framework import serializers

from .models import Compra, Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "descripcion", "precio", "stock"]


class CompraRequestSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)


class CompraSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "producto", "cantidad", "total", "creada_en"]
