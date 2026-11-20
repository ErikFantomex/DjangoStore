"""
URL mappings for the recipe app.
"""
from django.urls import(
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipes',views.RecipeViewSet)
router.register('tags',views.TagViewSet)
router.register('ingredients',views.IngredientViewSet)
router.register('meal',views.MealViewSet)
router.register('mealplans', views.MealPlanViewSet)  # Agrega esta línea


app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]