from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
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


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ComprarView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get(self, request):
        productos = Producto.objects.all()
        if request.accepted_renderer.format == "html":
            return Response(
                {"productos": productos},
                template_name="store/tienda.html",
            )
        return Response(ProductoSerializer(productos, many=True).data)

    def post(self, request):
        request_serializer = CompraRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        compra = comprar_producto(**request_serializer.validated_data)
        return Response(
            CompraSerializer(compra).data,
            status=status.HTTP_201_CREATED,
        )
