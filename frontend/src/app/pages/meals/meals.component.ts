import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { Meal } from '../../core/models';
import { newRecordCode } from '../../core/record-code';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './meals.component.html',
  styleUrl: './meals.component.scss'
})
export class MealsComponent implements OnInit {
  private fb = inject(FormBuilder);
  api = inject(ApiService);
  meals: Meal[] = [];
  editingId: number | null = null;
  error = '';
  form = this.fb.nonNullable.group({
    meal_id: '',
    name: ['', Validators.required]
  });

  ngOnInit(): void { this.load(); }
  load(): void { this.api.meals().subscribe(items => this.meals = items); }

  submit(): void {
    if (this.form.invalid) return;
    const payload = this.form.getRawValue();
    if (!payload.meal_id) payload.meal_id = newRecordCode();
    const request = this.editingId
      ? this.api.updateMeal(this.editingId, payload)
      : this.api.createMeal(payload);
    request.subscribe({
      next: () => { this.reset(); this.load(); },
      error: () => this.error = 'No se pudo guardar la comida.'
    });
  }

  edit(meal: Meal): void {
    this.editingId = meal.id ?? null;
    this.form.patchValue({ meal_id: meal.meal_id, name: meal.name });
  }

  reset(): void {
    this.editingId = null;
    this.error = '';
    this.form.reset({ meal_id: '', name: '' });
  }

  remove(meal: Meal): void {
    if (!meal.id || !confirm(`Eliminar "${meal.name}"?`)) return;
    this.api.deleteMeal(meal.id).subscribe(() => this.load());
  }
}
