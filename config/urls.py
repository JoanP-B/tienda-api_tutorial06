from django.contrib import admin
from django.urls import include, path

from store.views import tienda


urlpatterns = [
    path("", tienda, name="tienda"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("store.urls")),
]
