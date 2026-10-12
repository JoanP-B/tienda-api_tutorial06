from django.urls import path

from .views import ComprarView


urlpatterns = [
    path("comprar/", ComprarView.as_view(), name="comprar"),
]
