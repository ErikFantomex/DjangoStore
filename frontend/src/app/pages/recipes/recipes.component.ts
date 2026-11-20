import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { Ingredient, Recipe, Tag } from '../../core/models';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './recipes.component.html',
  styleUrl: './recipes.component.scss'
})
export class RecipesComponent implements OnInit {
  private fb = inject(FormBuilder);
  api = inject(ApiService);
  recipes: Recipe[] = [];
  tags: Tag[] = [];
  ingredients: Ingredient[] = [];
  editingId: number | null = null;
  error = '';
  form = this.fb.nonNullable.group({
    title: ['', Validators.required],
    meal_id: ['', Validators.required],
    description: '',
    image_url: ['', Validators.required],
    isMealPrepRecipe: false,
    time_minutes: [20, [Validators.required, Validators.min(1)]],
    price_level: [3, [Validators.required, Validators.min(1), Validators.max(5)]],
    instructions: ['', Validators.required],
    tagsText: '',
    ingredientsText: '',
    nutritionalInfo: ['{}', Validators.required]
  });

  ngOnInit(): void { this.load(); }

  load(): void {
    this.api.recipes().subscribe(items => this.recipes = items);
    this.api.tags().subscribe(items => this.tags = items);
    this.api.ingredients().subscribe(items => this.ingredients = items);
  }

  edit(recipe: Recipe): void {
    this.editingId = recipe.id ?? null;
    this.form.patchValue({
      title: recipe.title,
      meal_id: recipe.meal_id,
      description: recipe.description || '',
      image_url: recipe.image_url,
      isMealPrepRecipe: recipe.isMealPrepRecipe,
      time_minutes: recipe.time_minutes,
      price_level: recipe.price_level,
      instructions: recipe.instructions,
      tagsText: (recipe.tags || []).map(tag => tag.name).join(', '),
      ingredientsText: (recipe.ingredients || []).map(item => `${item.label}|${item.amount}|${item.unit}`).join('\n'),
      nutritionalInfo: JSON.stringify(recipe.nutritionalInfo || {}, null, 2)
    });
  }

  reset(): void {
    this.editingId = null;
    this.error = '';
    this.form.reset({
      title: '', meal_id: '', description: '', image_url: '',
      isMealPrepRecipe: false, time_minutes: 20, price_level: 3,
      instructions: '', tagsText: '', ingredientsText: '', nutritionalInfo: '{}'
    });
  }

  submit(): void {
    if (this.form.invalid) return;
    let nutritionalInfo: Record<string, unknown>;
    try { nutritionalInfo = JSON.parse(this.form.controls.nutritionalInfo.value); }
    catch { this.error = 'La informacion nutricional debe ser JSON valido.'; return; }
    const value = this.form.getRawValue();
    const payload: Recipe = {
      meal_id: value.meal_id,
      title: value.title,
      description: value.description,
      image_url: value.image_url,
      isMealPrepRecipe: value.isMealPrepRecipe,
      time_minutes: value.time_minutes,
      price_level: value.price_level,
      instructions: value.instructions,
      nutritionalInfo,
      tags: value.tagsText.split(',').map(name => name.trim()).filter(Boolean).map(name => ({ name })),
      ingredients: value.ingredientsText.split('\n').map(line => line.trim()).filter(Boolean).map(line => {
        const [label, amount, unit] = line.split('|').map(part => part.trim());
        return { label, amount: amount || '1', unit: unit || 'unidad' };
      })
    };
    const request = this.editingId
      ? this.api.updateRecipe(this.editingId, payload)
      : this.api.createRecipe(payload);
    request.subscribe({
      next: () => { this.reset(); this.load(); },
      error: () => this.error = 'No se pudo guardar la receta. Revisa los datos.'
    });
  }

  remove(recipe: Recipe): void {
    if (!recipe.id || !confirm(`Eliminar "${recipe.title}"?`)) return;
    this.api.deleteRecipe(recipe.id).subscribe(() => this.load());
  }
}
