import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);
  error = '';
  form = this.fb.nonNullable.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(5)]]
  });

  submit(): void {
    if (this.form.invalid) return;
    this.error = '';
    this.auth.register(this.form.getRawValue()).subscribe({
      next: () => {
        const { email, password } = this.form.getRawValue();
        this.auth.login(email, password).subscribe(() => this.router.navigate(['/']));
      },
      error: () => this.error = 'No se pudo crear la cuenta. Revisa los datos.'
    });
  }
}
