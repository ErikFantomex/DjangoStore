import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { MealPlan } from '../../core/models';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './meal-plans.component.html',
  styleUrl: './meal-plans.component.scss'
})
export class MealPlansComponent implements OnInit {
  private fb = inject(FormBuilder);
  api = inject(ApiService);
  plans: MealPlan[] = [];
  editingId: number | null = null;
  error = '';
  days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  form = this.fb.nonNullable.group({
    meal_plan_id: ['', Validators.required],
    client_name: ['', Validators.required],
    client_weight: [70, [Validators.required, Validators.min(.1)]],
    client_height: [170, [Validators.required, Validators.min(.1)]],
    plan_type: ['', Validators.required],
    plan_length_in_weeks: [4, [Validators.required, Validators.min(1)]],
    current_week: [1, [Validators.required, Validators.min(1)]],
    tracking_days: [['Monday'], Validators.required],
    prep_day: ['Monday', Validators.required],
    daily_goals: ['{}', Validators.required],
    meals_per_day: ['{}', Validators.required],
    meals: ['{}', Validators.required]
  });

  ngOnInit(): void { this.load(); }
  load(): void { this.api.mealPlans().subscribe(items => this.plans = items); }

  toggleDay(day: string): void {
    const selected = [...this.form.controls.tracking_days.value];
    const next = selected.includes(day) ? selected.filter(item => item !== day) : [...selected, day];
    this.form.controls.tracking_days.setValue(next);
  }

  edit(plan: MealPlan): void {
    this.editingId = plan.id ?? null;
    this.form.patchValue({
      meal_plan_id: plan.meal_plan_id,
      client_name: plan.client_name,
      client_weight: plan.client_weight,
      client_height: plan.client_height,
      plan_type: plan.plan_type,
      plan_length_in_weeks: plan.plan_length_in_weeks,
      current_week: plan.current_week,
      tracking_days: plan.tracking_days,
      prep_day: plan.prep_day,
      daily_goals: JSON.stringify(plan.daily_goals || {}, null, 2),
      meals_per_day: JSON.stringify(plan.meals_per_day || {}, null, 2),
      meals: JSON.stringify(plan.meals || {}, null, 2)
    });
  }

  reset(): void {
    this.editingId = null;
    this.error = '';
    this.form.reset({
      meal_plan_id: '', client_name: '', client_weight: 70, client_height: 170,
      plan_type: '', plan_length_in_weeks: 4, current_week: 1,
      tracking_days: ['Monday'], prep_day: 'Monday',
      daily_goals: '{}', meals_per_day: '{}', meals: '{}'
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    let daily_goals: Record<string, unknown>;
    let meals_per_day: Record<string, unknown>;
    let meals: Record<string, unknown>;
    try {
      daily_goals = JSON.parse(this.form.controls.daily_goals.value);
      meals_per_day = JSON.parse(this.form.controls.meals_per_day.value);
      meals = JSON.parse(this.form.controls.meals.value);
    } catch {
      this.error = 'Los objetivos y comidas deben ser JSON valido.';
      return;
    }
    const value = this.form.getRawValue();
    const payload: MealPlan = {
      meal_plan_id: value.meal_plan_id,
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
      meals
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
