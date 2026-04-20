import { ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { ErrorMessageService } from '../../services/error-message.service';

@Component({
  selector: 'app-auth',
  imports: [CommonModule, FormsModule],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css',
})
export class AuthComponent {
  loginForm = {
    username: '',
    password: '',
  };
  registerForm = {
    username: '',
    email: '',
    password: '',
    favoriteTeam: '',
  };
  errorMessage = '';
  successMessage = '';

  constructor(
    private authService: AuthService,
    private errorMessageService: ErrorMessageService,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {}

  login(): void {
    this.errorMessage = '';
    this.successMessage = '';
    this.authService.login(this.loginForm).subscribe({
      next: () => {
        this.successMessage = 'Logged in successfully.';
        this.cdr.detectChanges();
        this.router.navigate(['/posts']);
      },
      error: (error) => {
        this.errorMessage = this.errorMessageService.extract(error);
        this.cdr.detectChanges();
      },
    });
  }

  register(): void {
    this.errorMessage = '';
    this.successMessage = '';
    this.authService
      .register({
        username: this.registerForm.username,
        email: this.registerForm.email,
        password: this.registerForm.password,
      })
      .subscribe({
        next: () => {
          this.successMessage = `Welcome ${this.registerForm.username}. Favorite team noted: ${this.registerForm.favoriteTeam || 'none yet'}.`;
          this.cdr.detectChanges();
          this.router.navigate(['/posts']);
        },
        error: (error) => {
          this.errorMessage = this.errorMessageService.extract(error);
          this.cdr.detectChanges();
        },
      });
  }
}
