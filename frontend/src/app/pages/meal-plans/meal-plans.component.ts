import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { newRecordCode } from '../../core/record-code';
import { Meal, MealPlan } from '../../core/models';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './meal-plans.component.html',
  styleUrl: './meal-plans.component.scss'
})
export class MealPlansComponent implements OnInit {
  private fb = inject(FormBuilder);
  api = inject(ApiService);
  plans: MealPlan[] = [];
  meals: Meal[] = [];
  weeklyMenu: MealPlan['meals'] = {};
  private savedGoals: MealPlan['daily_goals'] = {};
  private savedMealTimes: MealPlan['meals_per_day'] = {};
  editingId: number | null = null;
  error = '';
  days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  dayNames = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
  goalFields = [
    { key: 'calories', label: 'Energía (kcal)' }, { key: 'protein', label: 'Proteínas (g)' },
    { key: 'carbs', label: 'Carbohidratos (g)' }, { key: 'fat', label: 'Grasas (g)' }
  ] as const;
  mealTimes = [
    { key: 'breakfast', label: 'Desayuno' }, { key: 'lunch', label: 'Comida' },
    { key: 'dinner', label: 'Cena' }, { key: 'snacks', label: 'Colaciones' }
  ] as const;
  form = this.fb.nonNullable.group({
    meal_plan_id: '',
    client_name: ['', Validators.required],
    client_weight: [70, [Validators.required, Validators.min(.1)]],
    client_height: [170, [Validators.required, Validators.min(.1)]],
    plan_type: ['', Validators.required],
    plan_length_in_weeks: [4, [Validators.required, Validators.min(1)]],
    current_week: [1, [Validators.required, Validators.min(1)]],
    tracking_days: [['Monday'], Validators.required],
    prep_day: ['Monday', Validators.required],
    goals: this.fb.group({
      calories: this.fb.control<number | null>(null, Validators.min(0)),
      protein: this.fb.control<number | null>(null, Validators.min(0)),
      carbs: this.fb.control<number | null>(null, Validators.min(0)),
      fat: this.fb.control<number | null>(null, Validators.min(0))
    }),
    mealTimes: this.fb.nonNullable.group({ breakfast: false, lunch: false, dinner: false, snacks: false })
  });

  ngOnInit(): void {
    this.load();
    this.api.meals().subscribe(items => this.meals = items);
  }
  load(): void { this.api.mealPlans().subscribe(items => this.plans = items); }

  toggleDay(day: string): void {
    const selected = [...this.form.controls.tracking_days.value];
    const next = selected.includes(day) ? selected.filter(item => item !== day) : [...selected, day];
    this.form.controls.tracking_days.setValue(next);
  }

  menuFor(day: number): string[] {
    const meals = this.weeklyMenu[`day${day + 1}`];
    return Array.isArray(meals) ? meals : [];
  }

  toggleMeal(day: number, code: string): void {
    const selected = this.menuFor(day);
    this.weeklyMenu[`day${day + 1}`] = selected.includes(code)
      ? selected.filter(item => item !== code) : [...selected, code];
  }

  edit(plan: MealPlan): void {
    this.reset();
    this.editingId = plan.id ?? null;
    this.savedGoals = plan.daily_goals || {};
    this.savedMealTimes = plan.meals_per_day || {};
    this.weeklyMenu = { ...plan.meals };
    this.form.patchValue({
      meal_plan_id: plan.meal_plan_id,
      client_name: plan.client_name,
      client_weight: plan.client_weight,
      client_height: plan.client_height,
      plan_type: plan.plan_type,
      plan_length_in_weeks: plan.plan_length_in_weeks,
      current_week: plan.current_week,
      tracking_days: plan.tracking_days,
      prep_day: plan.prep_day
    });
    for (const { key } of this.goalFields) {
      const value = this.savedGoals[key];
      if (typeof value === 'number') this.form.controls.goals.controls[key].setValue(value);
    }
    for (const { key } of this.mealTimes) {
      this.form.controls.mealTimes.controls[key].setValue(this.savedMealTimes[key] === true);
    }
  }

  reset(): void {
    this.editingId = null;
    this.error = '';
    this.form.reset();
    this.savedGoals = {};
    this.savedMealTimes = {};
    this.weeklyMenu = {};
  }

  submit(): void {
    if (this.form.invalid) return;
    const value = this.form.getRawValue();
    if (value.current_week > value.plan_length_in_weeks) {
      this.error = 'La semana actual debe estar dentro de la duración del plan.';
      return;
    }
    const daily_goals = { ...this.savedGoals };
    const meals_per_day = { ...this.savedMealTimes };
    for (const { key } of this.goalFields) {
      if (!this.form.controls.goals.controls[key].dirty) continue;
      if (value.goals[key] === null) delete daily_goals[key];
      else daily_goals[key] = value.goals[key];
    }
    for (const { key } of this.mealTimes) {
      if (this.form.controls.mealTimes.controls[key].dirty) meals_per_day[key] = value.mealTimes[key];
    }
    const payload: MealPlan = {
      meal_plan_id: value.meal_plan_id || newRecordCode(),
      client_name: value.client_name,
      client_weight: value.client_weight,
      client_height: value.client_height,
      plan_type: value.plan_type,
      plan_length_in_weeks: value.plan_length_in_weeks,
      current_week: value.current_week,
      tracking_days: value.tracking_days,
      prep_day: value.prep_day,
      daily_goals,
      meals_per_day,
      meals: this.weeklyMenu
    };
    const request = this.editingId
      ? this.api.updateMealPlan(this.editingId, payload)
      : this.api.createMealPlan(payload);
    request.subscribe({
      next: () => { this.reset(); this.load(); },
      error: () => this.error = 'No se pudo guardar el plan. Revisa semana, medidas y dias.'
    });
  }

  remove(plan: MealPlan): void {
    if (!plan.id || !confirm(`Eliminar el plan de ${plan.client_name}?`)) return;
    this.api.deleteMealPlan(plan.id).subscribe(() => this.load());
  }
}
