import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { ApiService } from '../../core/api.service';
import { FoodProduct, FoodSummary } from '../../core/models';
import { CatalogProduct, PRODUCT_CATALOG } from './product-catalog';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './food-data.component.html',
  styleUrl: './food-data.component.scss'
})
export class FoodDataComponent implements OnInit {
  private api = inject(ApiService);
  search = '';
  category = 'Todos';
  visibleCount = 12;
  readonly categories = ['Todos', ...new Set(PRODUCT_CATALOG.map(product => product.category))];
  selectedProduct: CatalogProduct | null = null;
  products: FoodProduct[] = [];
  summary: FoodSummary = { count: 0, average_calories: null, average_protein: null };
  loading = false;
  importing = false;
  error = '';
  message = '';
  readonly placeholder = '/ingredients/placeholder.svg';

  get catalog(): readonly CatalogProduct[] {
    const normalize = (value: string) => value.toLowerCase().normalize('NFD').replace(/\p{M}/gu, '');
    const terms = normalize(this.search.trim()).split(/\s+/);
    return PRODUCT_CATALOG.filter(product => {
      const description = normalize(`${product.name} ${product.brand} ${product.description} ${product.category}`);
      return (this.category === 'Todos' || this.category === product.category)
        && terms.every(term => description.includes(term));
    });
  }

  ngOnInit(): void { this.reload(); }

  filterBy(category: string): void {
    this.category = category;
    this.visibleCount = 12;
  }

  reload(): void {
    this.loading = true;
    this.api.foodProducts().subscribe({
      next: products => { this.products = products; this.loading = false; },
      error: () => { this.error = 'No se pudieron cargar los productos guardados.'; this.loading = false; }
    });
    this.api.foodSummary().subscribe({ next: summary => this.summary = summary });
  }

  selectProduct(product: CatalogProduct): void {
    this.selectedProduct = product;
    this.error = '';
    this.message = '';
  }

  importProduct(): void {
    if (!this.selectedProduct || this.importing) return;
    this.error = '';
    this.message = '';
    this.importing = true;
    this.api.importFoodProduct(this.selectedProduct.barcode).subscribe({
      next: product => {
        this.message = `${product.name} ya está en la comparación.`;
        this.importing = false;
        this.reload();
      },
      error: (response: HttpErrorResponse) => {
        this.error = response.error?.detail || response.error?.barcode?.[0] || 'No se pudo importar el producto.';
        this.importing = false;
      }
    });
  }

  imageFor(product: FoodProduct): string {
    return product.image_url || PRODUCT_CATALOG.find(item => item.barcode === product.barcode)?.imageUrl || this.placeholder;
  }

  useFallback(event: Event): void {
    const image = event.target as HTMLImageElement;
    if (!image.src.endsWith(this.placeholder)) image.src = this.placeholder;
  }

  get chartProducts(): FoodProduct[] {
    return this.products.filter(item => item.calories_100g !== null)
      .sort((a, b) => (b.calories_100g ?? 0) - (a.calories_100g ?? 0)).slice(0, 10);
  }

  calorieWidth(product: FoodProduct): number {
    const max = Math.max(...this.chartProducts.map(item => item.calories_100g ?? 0), 1);
    return ((product.calories_100g ?? 0) / max) * 100;
  }

  macroWidth(value: number | null): number { return Math.min(Math.max(value ?? 0, 0), 100); }
}
