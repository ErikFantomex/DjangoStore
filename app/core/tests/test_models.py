"""
Test for models .
Pruebas para modelos
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from core.models import Meal, MealPlan


def create_user(email='user@example.com', password='testpass123'):
    """Crea y regresa un nuevo usuario."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Pruebas para los modelos"""

    def test_create_user_with_email_successful(self):
        """Test para verificar que se crea un usuario con un correo exitosamente."""
        email = 'horacio.araiza.gonzalez@gmail.com'
        password = 'Chamebador123'
        user = create_user(email, password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Prueba para verificar que el correo de un nuevo usuario es normalizado."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['test3@EXAMPLE.com', 'test3@example.com'],
            ['test4@EXAMPLE.com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Prueba para verificar que crear un usuario sin correo devuelve un error."""
        with self.assertRaises(ValueError):
            create_user('', 'test123')

    def test_create_superuser(self):
        """Prueba para verificar la creación de un superusuario."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Prueba creando una receta exitosamente."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Vegano')
        ingredient = models.Ingredient.objects.create(
            user=user,
            label='Tomate',
            amount="2",
            unit="Unidades"
        )

        recipe = models.Recipe.objects.create(
            user=user,
            meal_id="ID12345",
            title='Nombre de receta de ejemplo',
            image_url='https://example.com/image.jpg',
            isMealPrepRecipe=True,
            time_minutes=10,
            price_level=2,
            instructions="Estas son las instrucciones de la receta.",
            nutritionalInfo={
                "calories": 100,
                "fat": "10g",
                "protein": "5g"
            }
        )
        recipe.tags.add(tag)
        recipe.ingredients.add(ingredient)

        self.assertEqual(str(recipe), recipe.title)
        self.assertIn(tag, recipe.tags.all())
        self.assertIn(ingredient, recipe.ingredients.all())


    def test_create_tag(self):
        """Prueba para verificar que se crea una etiqueta exitosamente."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Prueba creando un ingrediente exitosamente."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            label='Ingredient1',
            amount="100",
            unit="grams"
        )
        self.assertEqual(str(ingredient), ingredient.label)

class MealAndMealPlanModelTests(TestCase):
    """Pruebas para los modelos Meal y MealPlan"""

    def test_create_meal(self):
        """Prueba para verificar que se crea una comida correctamente."""
        user = create_user()
        meal = Meal.objects.create(
            meal_id="M001",
            name="Ensalada Caesar",
            user=user,
        )
        self.assertEqual(meal.meal_id, "M001")
        self.assertEqual(meal.name, "Ensalada Caesar")

    def test_create_mealplan(self):
        """Prueba para verificar que se crea un plan de comidas correctamente."""
        user = create_user()
        meal_plan = MealPlan.objects.create(
            user=user,
            meal_plan_id="MP001",
            client_name="Juan",
            client_weight=70.5,
            client_height=175.2,
            plan_type="Balanceado",
            plan_length_in_weeks=4,
            current_week=1,
            tracking_days=[
                "Monday",
                "Tuesday",
                "Friday",
            ],
            prep_day="Monday",
            daily_goals={
                "calories": 2000,
                "protein": 100,
                "fat": 70,
                "carbs": 250
            },
            meals_per_day={
                "breakfast": True,
                "lunch": True,
                "dinner": True,
                "snacks": False
            },
            meals={
                "day1": ["M001", "M002"],
                "day2": ["M003", "M004"]
            }
        )
        self.assertEqual(meal_plan.meal_plan_id, "MP001")
        self.assertEqual(meal_plan.client_name, "Juan")
        self.assertEqual(meal_plan.client_weight, 70.5)
        self.assertEqual(meal_plan.client_height, 175.2)
        self.assertEqual(meal_plan.plan_type, "Balanceado")
        self.assertEqual(meal_plan.plan_length_in_weeks, 4)
        self.assertEqual(meal_plan.current_week, 1)
        self.assertEqual(meal_plan.prep_day, "Monday")
        self.assertEqual(meal_plan.tracking_days, [
            "Monday",
            "Tuesday",
            "Friday",
        ])
        self.assertDictEqual(meal_plan.daily_goals, {
            "calories": 2000,
            "protein": 100,
            "fat": 70,
            "carbs": 250
        })
        self.assertDictEqual(meal_plan.meals_per_day, {
            "breakfast": True,
            "lunch": True,
            "dinner": True,
            "snacks": False
        })
        self.assertDictEqual(meal_plan.meals, {
            "day1": ["M001", "M002"],
            "day2": ["M003", "M004"]
        })