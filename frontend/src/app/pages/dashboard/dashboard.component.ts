import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  api = inject(ApiService);
  auth = inject(AuthService);
  recipes = 0;
  plans = 0;
  meals = 0;
  name = '';

  ngOnInit(): void {
    this.auth.profile().subscribe(profile => this.name = profile.name || profile.email);
    this.api.recipes().subscribe(items => this.recipes = items.length);
    this.api.mealPlans().subscribe(items => this.plans = items.length);
    this.api.meals().subscribe(items => this.meals = items.length);
  }
}
