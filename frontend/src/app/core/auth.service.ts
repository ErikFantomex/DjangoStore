import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { UserProfile } from './models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private tokenKey = 'auth_token';

  get token(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  get isAuthenticated(): boolean {
    return !!this.token;
  }

  login(email: string, password: string): Observable<{ token: string }> {
    return this.http.post<{ token: string }>('/api/user/token/', { email, password }).pipe(
      tap(result => localStorage.setItem(this.tokenKey, result.token))
    );
  }

  register(payload: UserProfile & { password: string }): Observable<UserProfile> {
    return this.http.post<UserProfile>('/api/user/create/', payload);
  }

  profile(): Observable<UserProfile> {
    return this.http.get<UserProfile>('/api/user/me/');
  }

  updateProfile(payload: UserProfile): Observable<UserProfile> {
    return this.http.patch<UserProfile>('/api/user/me/', payload);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.router.navigate(['/login']);
  }
}
