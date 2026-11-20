import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';
import { guestGuard } from './core/guest.guard';
import { ShellComponent } from './shell/shell.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { RecipesComponent } from './pages/recipes/recipes.component';
import { MealPlansComponent } from './pages/meal-plans/meal-plans.component';
import { MealsComponent } from './pages/meals/meals.component';
import { ProfileComponent } from './pages/profile/profile.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent, canActivate: [guestGuard] },
  { path: 'registro', component: RegisterComponent, canActivate: [guestGuard] },
  {
    path: '',
    component: ShellComponent,
    canActivate: [authGuard],
    children: [
      { path: '', component: DashboardComponent },
      { path: 'recetas', component: RecipesComponent },
      { path: 'planes', component: MealPlansComponent },
      { path: 'comidas', component: MealsComponent },
      { path: 'perfil', component: ProfileComponent }
    ]
  },
  { path: '**', redirectTo: '' }
];
