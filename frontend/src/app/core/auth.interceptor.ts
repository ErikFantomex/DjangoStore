import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);
  if (!auth.token) return next(request);
  return next(request.clone({
    setHeaders: { Authorization: `Token ${auth.token}` }
  }));
};
