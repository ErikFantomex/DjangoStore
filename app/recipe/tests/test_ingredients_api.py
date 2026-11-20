from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class IngredientApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='ingredients@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_auth_is_required(self):
        response = APIClient().get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ingredients_are_limited_to_owner(self):
        Ingredient.objects.create(
            user=self.user,
            label='Tomate',
            amount='100',
            unit='g',
        )
        other = get_user_model().objects.create_user(
            email='other-ingredients@example.com',
            password='testpass123',
        )
        Ingredient.objects.create(
            user=other,
            label='Pollo',
            amount='200',
            unit='g',
        )
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], 'Tomate')

    def test_update_and_delete_ingredient(self):
        ingredient = Ingredient.objects.create(
            user=self.user,
            label='Cebolla',
            amount='1',
            unit='unidad',
        )
        url = reverse('recipe:ingredient-detail', args=[ingredient.pk])
        response = self.client.patch(url, {'label': 'Cebolla morada'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.label, 'Cebolla morada')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
