from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Producto
from .serializers import (
    CompraRequestSerializer,
    CompraSerializer,
    ProductoSerializer,
)
from .services import comprar_producto


@ensure_csrf_cookie
def tienda(request):
    return render(
        request,
        "store/tienda.html",
        {"productos": Producto.objects.all()},
    )


def api_documentacion(request):
    return render(request, "store/api_docs.html")


class ProductosView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        productos = Producto.objects.all()
        return Response(ProductoSerializer(productos, many=True).data)


class ComprarView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        request_serializer = CompraRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        compra = comprar_producto(**request_serializer.validated_data)
        return Response(
            CompraSerializer(compra).data,
            status=status.HTTP_201_CREATED,
        )
