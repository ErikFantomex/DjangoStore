import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../core/auth.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent implements OnInit {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  message = '';
  form = this.fb.nonNullable.group({
    name: '',
    email: ['', Validators.required],
    password: ''
  });

  ngOnInit(): void {
    this.auth.profile().subscribe(profile => this.form.patchValue(profile));
  }

  submit(): void {
    if (this.form.invalid) return;
    const payload = this.form.getRawValue();
    this.auth.updateProfile({
      name: payload.name,
      email: payload.email,
      ...(payload.password ? { password: payload.password } : {})
    }).subscribe(() => {
      this.message = 'Perfil actualizado.';
      this.form.patchValue({ password: '' });
    });
  }
}
