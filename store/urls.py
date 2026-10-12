from django.urls import path

from .views import ComprarView, ProductosView


urlpatterns = [
    path("productos/", ProductosView.as_view(), name="productos"),
    path("comprar/", ComprarView.as_view(), name="comprar"),
]
