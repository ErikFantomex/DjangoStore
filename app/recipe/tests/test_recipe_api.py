from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Meal, MealPlan, Recipe


RECIPES_URL = reverse('recipe:recipe-list')
MEALS_URL = reverse('recipe:meal-list')
MEALPLANS_URL = reverse('recipe:mealplan-list')


def create_recipe(user, **params):
    defaults = {
        'title': 'Receta de prueba',
        'meal_id': '12345',
        'time_minutes': 20,
        'price_level': 3,
        'image_url': 'https://example.com/recipe.jpg',
        'isMealPrepRecipe': False,
        'instructions': 'Preparar y servir.',
        'nutritionalInfo': {'calories': 250},
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class RecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_auth_is_required(self):
        client = APIClient()
        response = client.get(RECIPES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_list_is_limited_to_owner(self):
        create_recipe(self.user)
        other = get_user_model().objects.create_user(
            email='other@example.com',
            password='testpass123',
        )
        create_recipe(other)
        response = self.client.get(RECIPES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Receta de prueba')

    def test_create_recipe_with_tags_and_ingredients(self):
        payload = {
            'title': 'Ensalada',
            'meal_id': '123',
            'time_minutes': 10,
            'price_level': 2,
            'image_url': 'https://example.com/salad.jpg',
            'isMealPrepRecipe': False,
            'instructions': 'Mezclar.',
            'nutritionalInfo': {'calories': 150},
            'tags': [{'name': 'Ligera'}],
            'ingredients': [{
                'label': 'Lechuga',
                'amount': '100',
                'unit': 'g',
            }],
        }
        response = self.client.post(
            RECIPES_URL,
            payload,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(pk=response.data['id'])
        self.assertEqual(recipe.user, self.user)
        self.assertTrue(recipe.tags.filter(name='Ligera').exists())
        self.assertTrue(recipe.ingredients.filter(label='Lechuga').exists())

    def test_update_is_limited_to_owner(self):
        other = get_user_model().objects.create_user(
            email='other@example.com',
            password='testpass123',
        )
        recipe = create_recipe(other)
        url = reverse('recipe:recipe-detail', args=[recipe.pk])
        response = self.client.patch(url, {'title': 'No permitida'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, 'Receta de prueba')

    def test_recommend_recipes_by_ingredients(self):
        recipe = create_recipe(self.user)
        ingredient = Ingredient.objects.create(
            user=self.user,
            label='Lechuga',
            amount='100',
            unit='g',
        )
        recipe.ingredients.add(ingredient)

        response = self.client.post(
            '/api/recipe/recipes/recommend/',
            {'ingredients': ['Lechuga', 'Tomate']},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Receta de prueba')
        self.assertGreater(response.data[0]['match_score'], 0)

    def test_new_account_gets_ideas_and_can_match_ingredient_aliases(self):
        url = '/api/recipe/recipes/recommend/'
        initial = self.client.post(url, {'ingredients': []}, format='json')
        self.assertEqual(initial.status_code, status.HTTP_200_OK)
        self.assertTrue(initial.data)
        self.assertTrue(initial.data[0]['instructions'])
        self.assertFalse(Recipe.objects.filter(user=self.user).exists())

        ingredients = ['TORTILLAS', 'nopal', 'queso panela', ' Jitomate ', 'pera']
        response = self.client.post(url, {'ingredients': ingredients}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first = response.data[0]
        self.assertEqual(first['title'], 'Tacos de nopal y queso panela')
        self.assertEqual(first['match_score'], 100)
        self.assertEqual(first['missing_ingredients'], [])
        self.assertIn('Tomate', first['matched_ingredients'])
        self.assertTrue(response.data[1]['missing_ingredients'])

    def test_reject_invalid_price_level(self):
        payload = {
            'title': 'Invalida',
            'meal_id': '123',
            'time_minutes': 10,
            'price_level': 9,
            'image_url': 'https://example.com/invalid.jpg',
            'instructions': 'No validar.',
            'nutritionalInfo': {},
        }
        response = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MealAndMealPlanApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='owner@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_meals_are_limited_to_owner(self):
        Meal.objects.create(
            meal_id='M001',
            name='Desayuno',
            user=self.user,
        )
        other = get_user_model().objects.create_user(
            email='owner2@example.com',
            password='testpass123',
        )
        Meal.objects.create(meal_id='M002', name='Cena', user=other)
        response = self.client.get(MEALS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mealplan_is_limited_to_owner(self):
        plan = MealPlan.objects.create(
            meal_plan_id='MP001',
            user=self.user,
            client_name='Juan',
            client_weight=70,
            client_height=175,
            plan_type='Balanceado',
            plan_length_in_weeks=4,
            current_week=1,
            tracking_days=['Monday', 'Tuesday'],
            prep_day='Monday',
            daily_goals={'calories': 2000},
            meals_per_day={'breakfast': True},
            meals={'day1': ['M001']},
        )
        url = reverse('recipe:mealplan-detail', args=[plan.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_access_mealplan(self):
        other = get_user_model().objects.create_user(
            email='owner3@example.com',
            password='testpass123',
        )
        plan = MealPlan.objects.create(
            meal_plan_id='MP002',
            user=other,
            client_name='Ana',
            client_weight=60,
            client_height=165,
            plan_type='Ligero',
            plan_length_in_weeks=4,
            current_week=1,
            tracking_days=['Monday'],
            prep_day='Monday',
            daily_goals={},
            meals_per_day={},
            meals={},
        )
        url = reverse('recipe:mealplan-detail', args=[plan.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mealplan_rejects_invalid_week(self):
        payload = {
            'meal_plan_id': 'MP003',
            'client_name': 'Luis',
            'client_weight': 80,
            'client_height': 180,
            'plan_type': 'Balanceado',
            'plan_length_in_weeks': 2,
            'current_week': 3,
            'tracking_days': ['Monday'],
            'prep_day': 'Monday',
            'daily_goals': {},
            'meals_per_day': {},
            'meals': {},
        }
        response = self.client.post(
            MEALPLANS_URL,
            payload,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
