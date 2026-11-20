import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CdkDragDrop, DragDropModule, moveItemInArray } from '@angular/cdk/drag-drop';
import { ApiService } from '../../core/api.service';
import { Ingredient, Recipe, Tag } from '../../core/models';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, DragDropModule],
  templateUrl: './recipes.component.html',
  styleUrl: './recipes.component.scss'
})
export class RecipesComponent implements OnInit {
  private fb = inject(FormBuilder);
  api = inject(ApiService);
  recipes: Recipe[] = [];
  tags: Tag[] = [];
  ingredients: Ingredient[] = [];
  selectedIngredients: Ingredient[] = [];
  recommendations: Recipe[] = [];
  recommendationsLoading = false;
  editingId: number | null = null;
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
    pimiento: 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa7e',
    cebolla: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655',
    champinon: 'https://images.unsplash.com/photo-1504545102780-26774c1bb073',
    coliflor: 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3',
    calabaza: 'https://images.unsplash.com/photo-1506915925760-8a8d1a4bca99',
    nopal: 'https://images.unsplash.com/photo-1566970653468-8eb9bd7b3ea9',
    naranja: 'https://images.unsplash.com/photo-1547514701-42782101795e',
    fresa: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6',
    mango: 'https://images.unsplash.com/photo-1553279768-865429fa0078',
    arandano: 'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea',
    pera: 'https://images.unsplash.com/photo-1567085184-c0e5f0eb0df2',
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
    tortilla: 'https://images.unsplash.com/photo-1624392141096-7a917049c6ce',
    'pasta integral': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141',
    leche: 'https://images.unsplash.com/photo-1550583724-b2692b85b150',
    'yogur natural': 'https://images.unsplash.com/photo-1571212515416-fca99f4de07c',
    'queso cottage': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da',
    'queso panela': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d',
    'frijol negro': 'https://images.unsplash.com/photo-1599909543561-1e5e3eb4a29c',
    garbanzo: 'https://images.unsplash.com/photo-1591758109093-5c3b9cf7d7f2',
    lenteja: 'https://images.unsplash.com/photo-1585996459328-8f9ca7aee4d9',
    haba: 'https://images.unsplash.com/photo-1620260528569-f3eb23c2d6fc',
    'aceite de oliva': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5',
    limón: 'https://images.unsplash.com/photo-1590502593747-42a996133562',
    ajo: 'https://images.unsplash.com/photo-1615477550927-6ec1d7e1e9cf',
    jengibre: 'https://images.unsplash.com/photo-1605502891375-7db4b0baf06b',
    canela: 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af'
  };
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

  visibleCatalogIngredients(): Ingredient[] {
    const query = this.catalogSearch.trim().toLowerCase();
    return this.catalogIngredients.filter(ingredient => {
      const matchesCategory =
        this.catalogCategory === 'Todos'
        || ingredient.category === this.catalogCategory;
      const matchesSearch =
        !query
        || ingredient.label.toLowerCase().includes(query);
      return matchesCategory && matchesSearch;
    });
  }

  load(): void {
    this.api.recipes().subscribe(items => this.recipes = items);
    this.api.tags().subscribe(items => this.tags = items);
    this.api.ingredients().subscribe(items => {
      this.ingredients = items;
      const knownLabels = new Set(this.catalogIngredients.map(item => item.label.toLowerCase()));
      for (const ingredient of items) {
        if (!knownLabels.has(ingredient.label.toLowerCase())) {
          this.catalogIngredients = [...this.catalogIngredients, ingredient];
          knownLabels.add(ingredient.label.toLowerCase());
        }
      }
    });
  }

  photoUrl(label: string): string {
    const photo = this.photoMap[label.trim().toLowerCase()];
    return `${photo || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c'}?auto=format&fit=crop&w=320&h=220&q=80`;
  }

  addIngredient(ingredient: Ingredient): void {
    const alreadySelected = this.selectedIngredients.some(
      item => item.label.toLowerCase() === ingredient.label.toLowerCase()
    );
    if (!alreadySelected) {
      this.selectedIngredients = [...this.selectedIngredients, { ...ingredient }];
      this.syncIngredientsText();
      this.refreshRecommendations();
    }
  }

  dropIngredient(event: CdkDragDrop<Ingredient[]>): void {
    const ingredient = event.item.data as Ingredient;
    if (event.previousIndex === event.currentIndex && event.previousContainer === event.container) return;
    if (!event.container.data?.length || event.previousContainer !== event.container) {
      this.addIngredient(ingredient);
    } else {
      moveItemInArray(this.selectedIngredients, event.previousIndex, event.currentIndex);
      this.syncIngredientsText();
    }
  }

  reorderIngredient(event: CdkDragDrop<Ingredient[]>): void {
    moveItemInArray(this.selectedIngredients, event.previousIndex, event.currentIndex);
    this.syncIngredientsText();
    this.refreshRecommendations();
  }

  removeSelectedIngredient(index: number): void {
    this.selectedIngredients.splice(index, 1);
    this.selectedIngredients = [...this.selectedIngredients];
    this.syncIngredientsText();
    this.refreshRecommendations();
  }

  updateIngredient(index: number, field: 'amount' | 'unit', value: string): void {
    this.selectedIngredients[index][field] = value;
    this.syncIngredientsText();
  }

  syncIngredientsText(): void {
    this.form.controls.ingredientsText.setValue(
      this.selectedIngredients
        .map(item => `${item.label}|${item.amount}|${item.unit}`)
        .join('\n')
    );
  }

  refreshRecommendations(): void {
    const labels = this.selectedIngredients.map(item => item.label);
    if (!labels.length) {
      this.recommendations = [];
      return;
    }
    this.recommendationsLoading = true;
    this.api.recommendRecipes(labels).subscribe({
      next: items => {
        this.recommendations = items;
        this.recommendationsLoading = false;
      },
      error: () => {
        this.recommendations = [];
        this.recommendationsLoading = false;
      }
    });
  }

  useRecommendation(recipe: Recipe): void {
    this.editingId = null;
    this.selectedIngredients = (recipe.ingredients || []).map(item => ({ ...item }));
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
      nutritionalInfo: JSON.stringify(recipe.nutritionalInfo || {}, null, 2)
    });
    this.syncIngredientsText();
  }

  edit(recipe: Recipe): void {
    this.editingId = recipe.id ?? null;
    this.selectedIngredients = (recipe.ingredients || []).map(item => ({ ...item }));
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
    this.refreshRecommendations();
  }

  reset(): void {
    this.editingId = null;
    this.selectedIngredients = [];
    this.recommendations = [];
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
