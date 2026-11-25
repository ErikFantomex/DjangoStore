from unittest.mock import patch

from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from core.models import User
from food.models import FoodProduct
from food.services import ProductNotFound, ProductSourceError


class FoodApiTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='demo@example.com', password='testpass123')
        token = Token.objects.create(user=user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    @patch('food.views.fetch_product')
    def test_import_persists_and_updates_without_duplicate(self, fetch):
        fetch.return_value = {
            'name': 'Producto de prueba', 'brand': 'Marca',
            'calories_100g': 100, 'protein_100g': 5,
            'carbohydrates_100g': 10, 'fat_100g': 3,
            'sugars_100g': None, 'nutriscore': 'b',
        }
        first = self.client.post('/api/food/products/import/', {'barcode': '3017620422003'})
        self.assertEqual(first.status_code, 201)
        fetch.return_value['calories_100g'] = 120
        second = self.client.post('/api/food/products/import/', {'barcode': '3017620422003'})
        self.assertEqual(second.status_code, 200)
        self.assertEqual(FoodProduct.objects.count(), 1)
        self.assertEqual(FoodProduct.objects.get().calories_100g, 120)
        self.assertEqual(self.client.get('/api/food/summary/').data['count'], 1)
        self.assertEqual(len(self.client.get('/api/food/products/').data), 1)

    @patch('food.views.fetch_product', side_effect=ProductNotFound('No encontrado'))
    def test_missing_product_does_not_write(self, fetch):
        response = self.client.post('/api/food/products/import/', {'barcode': '12345678'})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(FoodProduct.objects.exists())

    @patch('food.views.fetch_product', side_effect=ProductSourceError('API no disponible'))
    def test_source_failure_does_not_write(self, fetch):
        response = self.client.post('/api/food/products/import/', {'barcode': '12345678'})
        self.assertEqual(response.status_code, 502)
        self.assertFalse(FoodProduct.objects.exists())

    def test_rejects_invalid_barcode_and_requires_authentication(self):
        self.assertEqual(self.client.post('/api/food/products/import/', {'barcode': '../etc'}).status_code, 400)
        self.client.credentials()
        self.assertEqual(self.client.get('/api/food/products/').status_code, 401)
