from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Compra, Producto


class ComprarApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.producto = Producto.objects.create(
            nombre="Café EAFIT",
            descripcion="Café de prueba",
            precio=Decimal("18000.00"),
            stock=5,
        )

    def test_tienda_muestra_el_catalogo(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tu próxima")
        self.assertContains(response, "Café EAFIT")

    def test_get_lista_productos(self):
        response = self.client.get("/api/v1/comprar/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["nombre"], "Café EAFIT")

    def test_get_api_en_navegador_muestra_tienda(self):
        response = self.client.get(
            "/api/v1/comprar/",
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Elige algo que te inspire.")
        self.assertContains(response, "Café EAFIT")
        self.assertIn("csrftoken", response.cookies)

    def test_get_api_con_accept_json_conserva_respuesta_json(self):
        response = self.client.get(
            "/api/v1/comprar/",
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["nombre"], "Café EAFIT")

    def test_post_compra_reduce_stock_and_returns_total(self):
        response = self.client.post(
            "/api/v1/comprar/",
            {"producto_id": self.producto.id, "cantidad": 2},
            format="json",
        )

        self.producto.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["total"], "36000.00")
        self.assertEqual(self.producto.stock, 3)
        self.assertEqual(Compra.objects.count(), 1)

    def test_post_compra_rejects_quantity_above_stock(self):
        response = self.client.post(
            "/api/v1/comprar/",
            {"producto_id": self.producto.id, "cantidad": 6},
            format="json",
        )

        self.producto.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.producto.stock, 5)
        self.assertEqual(Compra.objects.count(), 0)
