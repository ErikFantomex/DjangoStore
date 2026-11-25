import { Component, DestroyRef, ElementRef, OnInit, ViewChild, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CdkDragDrop, DragDropModule, moveItemInArray } from '@angular/cdk/drag-drop';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { Subscription } from 'rxjs';
import { ApiService } from '../../core/api.service';
import { newRecordCode } from '../../core/record-code';
import { Ingredient, Recipe, RecipeSuggestion } from '../../core/models';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, DragDropModule, ScrollingModule],
  templateUrl: './recipes.component.html',
  styleUrl: './recipes.component.scss'
})
export class RecipesComponent implements OnInit {
  private fb = inject(FormBuilder);
  private destroyRef = inject(DestroyRef);
  private recommendationsRequest?: Subscription;
  @ViewChild('editorHeading') private set editorHeading(heading: ElementRef<HTMLElement> | undefined) {
    if (heading) requestAnimationFrame(() => heading.nativeElement.focus());
  }
  api = inject(ApiService);
  recipes: Recipe[] = [];
  selectedIngredients: Ingredient[] = [];
  recommendations: RecipeSuggestion[] = [];
  recommendationsLoading = false;
  recommendationError = false;
  editorOpen = false;
  saving = false;
  editingId: number | null = null;
  private recipeCode = '';
  private originalNutrition: Record<string, unknown> = {};
  readonly nutritionFields = [
    { key: 'calories', label: 'Energía (kcal)' },
    { key: 'protein', label: 'Proteínas (g)' },
    { key: 'carbohydrates', label: 'Carbohidratos (g)' },
    { key: 'fat', label: 'Grasas (g)' }
  ] as const;
  error = '';
  catalogSearch = '';
  catalogCategory = 'Todos';
  catalogCategories = [
    'Todos', 'Verduras', 'Frutas', 'Proteinas', 'Cereales',
    'Lacteos', 'Legumbres', 'Condimentos'
  ];
  catalogIngredients: Ingredient[] = [
    { label: 'Lechuga', amount: '100', unit: 'g', category: 'Verduras' },
    { label: 'Tomate', amount: '1', unit: 'pieza', category: 'Verduras' },
    { label: 'Aguacate', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Brocoli', amount: '100', unit: 'g', category: 'Verduras' },
    { label: 'Pepino', amount: '1', unit: 'pieza', category: 'Verduras' },
    { label: 'Zanahoria', amount: '1', unit: 'pieza', category: 'Verduras' },
    { label: 'Pimiento', amount: '1', unit: 'pieza', category: 'Verduras' },
    { label: 'Cebolla', amount: '1', unit: 'pieza', category: 'Verduras' },
    { label: 'Champinon', amount: '100', unit: 'g', category: 'Verduras' },
    { label: 'Coliflor', amount: '150', unit: 'g', category: 'Verduras' },
    { label: 'Calabaza', amount: '150', unit: 'g', category: 'Verduras' },
    { label: 'Espinaca', amount: '100', unit: 'g', category: 'Verduras' },
    { label: 'Nopal', amount: '100', unit: 'g', category: 'Verduras' },
    { label: 'Manzana', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Platano', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Naranja', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Fresa', amount: '100', unit: 'g', category: 'Frutas' },
    { label: 'Mango', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Arandano', amount: '50', unit: 'g', category: 'Frutas' },
    { label: 'Pera', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Sandia', amount: '200', unit: 'g', category: 'Frutas' },
    { label: 'Kiwi', amount: '1', unit: 'pieza', category: 'Frutas' },
    { label: 'Pollo', amount: '150', unit: 'g', category: 'Proteinas' },
    { label: 'Pescado', amount: '150', unit: 'g', category: 'Proteinas' },
    { label: 'Salmon', amount: '150', unit: 'g', category: 'Proteinas' },
    { label: 'Atun', amount: '100', unit: 'g', category: 'Proteinas' },
    { label: 'Carne de res', amount: '150', unit: 'g', category: 'Proteinas' },
    { label: 'Pavo', amount: '150', unit: 'g', category: 'Proteinas' },
    { label: 'Huevo', amount: '1', unit: 'pieza', category: 'Proteinas' },
    { label: 'Tofu', amount: '100', unit: 'g', category: 'Proteinas' },
    { label: 'Avena', amount: '50', unit: 'g', category: 'Cereales' },
    { label: 'Arroz', amount: '100', unit: 'g', category: 'Cereales' },
    { label: 'Quinoa', amount: '80', unit: 'g', category: 'Cereales' },
    { label: 'Pan integral', amount: '2', unit: 'rebanadas', category: 'Cereales' },
    { label: 'Tortilla', amount: '2', unit: 'piezas', category: 'Cereales' },
    { label: 'Pasta integral', amount: '100', unit: 'g', category: 'Cereales' },
    { label: 'Leche', amount: '250', unit: 'ml', category: 'Lacteos' },
    { label: 'Yogur natural', amount: '150', unit: 'g', category: 'Lacteos' },
    { label: 'Queso cottage', amount: '100', unit: 'g', category: 'Lacteos' },
    { label: 'Queso panela', amount: '80', unit: 'g', category: 'Lacteos' },
    { label: 'Frijol negro', amount: '100', unit: 'g', category: 'Legumbres' },
    { label: 'Garbanzo', amount: '100', unit: 'g', category: 'Legumbres' },
    { label: 'Lenteja', amount: '100', unit: 'g', category: 'Legumbres' },
    { label: 'Haba', amount: '100', unit: 'g', category: 'Legumbres' },
    { label: 'Aceite de oliva', amount: '1', unit: 'cda', category: 'Condimentos' },
    { label: 'Limón', amount: '1', unit: 'pieza', category: 'Condimentos' },
    { label: 'Ajo', amount: '1', unit: 'diente', category: 'Condimentos' },
    { label: 'Jengibre', amount: '10', unit: 'g', category: 'Condimentos' },
    { label: 'Canela', amount: '1', unit: 'cdita', category: 'Condimentos' }
  ];
  private photoMap: Record<string, string> = {
    lechuga: 'https://images.unsplash.com/photo-1622205313162-be1d5712a43f',
    tomate: 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337',
    aguacate: 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578',
    pollo: 'https://images.unsplash.com/photo-1532550907401-a500c9a57435',
    avena: 'https://images.unsplash.com/photo-1517673400267-0251440c45dc',
    arroz: 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6',
    huevo: 'https://images.unsplash.com/photo-1587486913049-53fc88980cfc',
    platano: 'https://images.unsplash.com/photo-1603833665858-e61d17a86224',
    manzana: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6',
    brocoli: 'https://images.unsplash.com/photo-1459411621453-7b03977f4bfc',
    espinaca: 'https://images.unsplash.com/photo-1576045057995-568f588f82fb',
    pepino: 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6',
    zanahoria: 'https://images.unsplash.com/photo-1447175008436-054170c2e979',
    pimiento: '/ingredients/pimiento.jpg',
    cebolla: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655',
    champinon: 'https://images.unsplash.com/photo-1504545102780-26774c1bb073',
    coliflor: 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3',
    calabaza: '/ingredients/calabaza.jpg',
    nopal: '/ingredients/nopal.jpg',
    naranja: 'https://images.unsplash.com/photo-1547514701-42782101795e',
    fresa: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6',
    mango: 'https://images.unsplash.com/photo-1553279768-865429fa0078',
    arandano: 'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea',
    pera: '/ingredients/pera.jpg',
    sandia: 'https://images.unsplash.com/photo-1563114773-84221bd62daa',
    kiwi: 'https://images.unsplash.com/photo-1585059895524-72359e06133a',
    pescado: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2',
    salmon: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288',
    atun: 'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c',
    'carne de res': 'https://images.unsplash.com/photo-1588347818036-558601350947',
    pavo: 'https://images.unsplash.com/photo-1598515214211-89d3c73ae83b',
    tofu: 'https://images.unsplash.com/photo-1564834724105-918b73d1b9e0',
    quinoa: 'https://images.unsplash.com/photo-1586201375761-83865001e31c',
    'pan integral': 'https://images.unsplash.com/photo-1509440159596-0249088772ff',
    tortilla: '/ingredients/tortilla.jpg',
    'pasta integral': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141',
    leche: 'https://images.unsplash.com/photo-1550583724-b2692b85b150',
    'yogur natural': '/ingredients/yogur-natural.jpg',
    'queso cottage': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da',
    'queso panela': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d',
    'frijol negro': '/ingredients/frijol-negro.jpg',
    garbanzo: '/ingredients/garbanzo.jpg',
    lenteja: '/ingredients/lenteja.jpg',
    haba: '/ingredients/haba.jpg',
    'aceite de oliva': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5',
    limon: 'https://images.unsplash.com/photo-1590502593747-42a996133562',
    ajo: '/ingredients/ajo.jpg',
    jengibre: '/ingredients/jengibre.jpg',
    canela: 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af'
  };
  form = this.fb.nonNullable.group({
    title: ['', Validators.required],
    description: '',
    image_url: '',
    isMealPrepRecipe: false,
    time_minutes: [20, [Validators.required, Validators.min(1)]],
    price_level: [3, [Validators.required, Validators.min(1), Validators.max(5)]],
    instructions: ['', Validators.required],
    tagsText: '',
    calories: this.fb.control<number | null>(null, Validators.min(0)),
    protein: this.fb.control<number | null>(null, Validators.min(0)),
    carbohydrates: this.fb.control<number | null>(null, Validators.min(0)),
    fat: this.fb.control<number | null>(null, Validators.min(0))
  });

  ngOnInit(): void { this.load(); this.refreshRecommendations(); }

  visibleCatalogIngredients(): Ingredient[] {
    const query = this.ingredientKey(this.catalogSearch);
    return this.catalogIngredients.filter(ingredient => {
      const matchesCategory =
        this.catalogCategory === 'Todos'
        || ingredient.category === this.catalogCategory;
      const matchesSearch =
        !query
        || this.ingredientKey(ingredient.label).includes(query);
      return matchesCategory && matchesSearch;
    });
  }

  load(): void {
    this.api.recipes().subscribe(items => this.recipes = items);
    this.api.ingredients().subscribe(items => {
      const knownLabels = new Set(this.catalogIngredients.map(item => this.ingredientKey(item.label)));
      for (const ingredient of items) {
        const key = this.ingredientKey(ingredient.label);
        if (!knownLabels.has(key)) {
          this.catalogIngredients = [...this.catalogIngredients, ingredient];
          knownLabels.add(key);
        }
      }
    });
  }

  photoUrl(label: string): string {
    const photo = this.photoMap[this.ingredientKey(label)];
    if (!photo) return '/ingredients/placeholder.svg';
    return photo.startsWith('/') ? photo : `${photo}?auto=format&fit=crop&w=320&h=220&q=80`;
  }

  private ingredientKey(label: string): string {
    return label.trim().toLowerCase().normalize('NFD').replace(/\p{M}/gu, '');
  }

  setPhotoFallback(event: Event): void {
    const image = event.target as HTMLImageElement;
    if (!image.src.endsWith('/ingredients/placeholder.svg')) {
      image.src = '/ingredients/placeholder.svg';
    }
  }

  isSelected(ingredient: Ingredient): boolean {
    return this.selectedIngredients.some(
      item => this.ingredientKey(item.label) === this.ingredientKey(ingredient.label)
    );
  }

  addIngredient(ingredient: Ingredient, index = this.selectedIngredients.length): void {
    if (this.isSelected(ingredient)) return;
    this.selectedIngredients.splice(index, 0, { ...ingredient });
    this.refreshRecommendations();
  }

  dropIngredient(event: CdkDragDrop<Ingredient[], Ingredient[], Ingredient>): void {
    if (!event.isPointerOverContainer) return;
    if (event.previousContainer !== event.container) {
      this.addIngredient(event.item.data, event.currentIndex);
      return;
    }
    moveItemInArray(this.selectedIngredients, event.previousIndex, event.currentIndex);
  }

  removeSelectedIngredient(index: number): void {
    this.selectedIngredients.splice(index, 1);
    this.selectedIngredients = [...this.selectedIngredients];
    this.refreshRecommendations();
  }

  updateIngredient(index: number, field: 'amount' | 'unit', value: string): void {
    this.selectedIngredients[index][field] = value;
  }

  refreshRecommendations(): void {
    this.recommendationsRequest?.unsubscribe();
    const labels = this.selectedIngredients.map(item => item.label);
    this.recommendationsLoading = true;
    this.recommendationError = false;
    this.recommendations = [];
    this.recommendationsRequest = this.api.recommendRecipes(labels)
      .pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: items => {
        this.recommendations = items;
        this.recommendationsLoading = false;
      },
      error: () => {
        this.recommendationError = true;
        this.recommendationsLoading = false;
      }
    });
  }

  useRecommendation(recipe: Recipe): void {
    this.openEditor(recipe, null);
  }

  edit(recipe: Recipe): void {
    this.openEditor(recipe, recipe.id ?? null);
  }

  openEditor(recipe?: Recipe, editingId: number | null = null): void {
    this.editingId = editingId;
    this.recipeCode = editingId ? recipe?.meal_id ?? '' : '';
    this.error = '';
    this.editorOpen = true;
    this.form.reset();
    this.originalNutrition = recipe?.nutritionalInfo || {};
    if (!recipe) return;
    this.selectedIngredients = (recipe.ingredients || []).map(item => ({ ...item }));
    this.form.patchValue({
      title: recipe.title,
      description: recipe.description || '',
      image_url: recipe.image_url,
      isMealPrepRecipe: recipe.isMealPrepRecipe,
      time_minutes: recipe.time_minutes,
      price_level: recipe.price_level,
      instructions: recipe.instructions,
      tagsText: (recipe.tags || []).map(tag => tag.name).join(', ')
    });
    for (const { key } of this.nutritionFields) {
      const value = this.originalNutrition[key];
      if (typeof value === 'number') this.form.controls[key].setValue(value);
    }
    this.refreshRecommendations();
  }

  reset(): void {
    this.editingId = null;
    this.editorOpen = false;
    this.selectedIngredients = [];
    this.refreshRecommendations();
    this.error = '';
    this.form.reset();
  }

  submit(): void {
    if (this.form.invalid || this.saving) return;
    const nutritionalInfo = { ...this.originalNutrition };
    for (const { key } of this.nutritionFields) {
      const control = this.form.controls[key];
      if (control.dirty) {
        if (control.value === null) delete nutritionalInfo[key];
        else nutritionalInfo[key] = control.value;
      }
    }
    const value = this.form.getRawValue();
    const payload: Recipe = {
      meal_id: this.recipeCode || newRecordCode(),
      title: value.title,
      description: value.description,
      image_url: value.image_url,
      isMealPrepRecipe: value.isMealPrepRecipe,
      time_minutes: value.time_minutes,
      price_level: value.price_level,
      instructions: value.instructions,
      nutritionalInfo,
      tags: value.tagsText.split(',').map(name => name.trim()).filter(Boolean).map(name => ({ name })),
      ingredients: this.selectedIngredients.map(({ label, amount, unit }) => ({
        label, amount: amount.trim() || '1', unit: unit.trim() || 'unidad'
      }))
    };
    const request = this.editingId
      ? this.api.updateRecipe(this.editingId, payload)
      : this.api.createRecipe(payload);
    this.saving = true;
    this.error = '';
    request.subscribe({
      next: () => { this.saving = false; this.reset(); this.load(); },
      error: () => {
        this.saving = false;
        this.error = 'No pudimos guardar tu receta. Revisa los datos e inténtalo de nuevo.';
      }
    });
  }

  remove(recipe: Recipe): void {
    if (!recipe.id || !confirm(`Eliminar "${recipe.title}"?`)) return;
    this.api.deleteRecipe(recipe.id).subscribe(() => this.load());
  }
}
