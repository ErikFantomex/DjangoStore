from django.urls import path

from core import views


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe-list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe-detail'),
    path('meals/<int:pk>/', views.meal_detail, name='meal-detail'),
    path('mealplans/', views.mealplan_list, name='mealplan-list'),
    path(
        'mealplans/<int:pk>/',
        views.mealplan_detail,
        name='mealplan-detail',
    ),
]
