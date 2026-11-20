import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ingredient, Meal, MealPlan, Recipe, Tag } from './models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);

  recipes(): Observable<Recipe[]> { return this.http.get<Recipe[]>('/api/recipe/recipes/'); }
  recipe(id: number): Observable<Recipe> { return this.http.get<Recipe>(`/api/recipe/recipes/${id}/`); }
  createRecipe(payload: Recipe): Observable<Recipe> { return this.http.post<Recipe>('/api/recipe/recipes/', payload); }
  recommendRecipes(ingredients: string[]): Observable<Recipe[]> {
    return this.http.post<Recipe[]>('/api/recipe/recipes/recommend/', { ingredients });
  }
  updateRecipe(id: number, payload: Partial<Recipe>): Observable<Recipe> { return this.http.patch<Recipe>(`/api/recipe/recipes/${id}/`, payload); }
  deleteRecipe(id: number): Observable<void> { return this.http.delete<void>(`/api/recipe/recipes/${id}/`); }

  tags(): Observable<Tag[]> { return this.http.get<Tag[]>('/api/recipe/tags/'); }
  createTag(name: string): Observable<Tag> { return this.http.post<Tag>('/api/recipe/tags/', { name }); }
  updateTag(id: number, name: string): Observable<Tag> { return this.http.patch<Tag>(`/api/recipe/tags/${id}/`, { name }); }
  deleteTag(id: number): Observable<void> { return this.http.delete<void>(`/api/recipe/tags/${id}/`); }

  ingredients(): Observable<Ingredient[]> { return this.http.get<Ingredient[]>('/api/recipe/ingredients/'); }
  createIngredient(payload: Ingredient): Observable<Ingredient> { return this.http.post<Ingredient>('/api/recipe/ingredients/', payload); }
  updateIngredient(id: number, payload: Ingredient): Observable<Ingredient> { return this.http.patch<Ingredient>(`/api/recipe/ingredients/${id}/`, payload); }
  deleteIngredient(id: number): Observable<void> { return this.http.delete<void>(`/api/recipe/ingredients/${id}/`); }

  meals(): Observable<Meal[]> { return this.http.get<Meal[]>('/api/recipe/meal/'); }
  createMeal(payload: Meal): Observable<Meal> { return this.http.post<Meal>('/api/recipe/meal/', payload); }
  updateMeal(id: number, payload: Meal): Observable<Meal> { return this.http.patch<Meal>(`/api/recipe/meal/${id}/`, payload); }
  deleteMeal(id: number): Observable<void> { return this.http.delete<void>(`/api/recipe/meal/${id}/`); }

  mealPlans(): Observable<MealPlan[]> { return this.http.get<MealPlan[]>('/api/recipe/mealplans/'); }
  createMealPlan(payload: MealPlan): Observable<MealPlan> { return this.http.post<MealPlan>('/api/recipe/mealplans/', payload); }
  updateMealPlan(id: number, payload: Partial<MealPlan>): Observable<MealPlan> { return this.http.patch<MealPlan>(`/api/recipe/mealplans/${id}/`, payload); }
  deleteMealPlan(id: number): Observable<void> { return this.http.delete<void>(`/api/recipe/mealplans/${id}/`); }
}
