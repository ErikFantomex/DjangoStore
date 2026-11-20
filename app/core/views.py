from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.models import Meal, MealPlan, Recipe


def home(request):
    return render(request, 'home.html')


@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(user=request.user).order_by('-id')
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    return render(request, 'recipe/recipe.detail.html', {'recipe': recipe})


@login_required
def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    return render(request, 'meal/meal_detail.html', {'meal': meal})


@login_required
def mealplan_list(request):
    mealplans = MealPlan.objects.filter(user=request.user).order_by('-id')
    return render(
        request,
        'mealplan/meal_plan_list.html',
        {'mealplans': mealplans},
    )


@login_required
def mealplan_detail(request, pk):
    mealplan = get_object_or_404(MealPlan, pk=pk, user=request.user)
    return render(
        request,
        'mealplan/meal_plan_detail.html',
        {'mealplan': mealplan},
    )
