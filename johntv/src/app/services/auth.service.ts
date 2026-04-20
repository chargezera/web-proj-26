import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, finalize, tap } from 'rxjs';

import { API_BASE_URL } from '../core/api.config';
import { AuthResponse, User } from '../models/auth.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly currentUserSignal = signal<User | null>(this.readUser());
  currentUser = this.currentUserSignal.asReadonly();

  constructor(private http: HttpClient) {}

  login(payload: { username: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${API_BASE_URL}/auth/login/`, payload).pipe(
      tap((response) => this.persistSession(response)),
    );
  }

  register(payload: { username: string; email: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${API_BASE_URL}/auth/register/`, payload).pipe(
      tap((response) => this.persistSession(response)),
    );
  }

  logout(): Observable<{ detail: string }> | null {
    const refresh = localStorage.getItem('johntv_refresh');

    if (!refresh) {
      this.clearSession();
      return null;
    }

    return this.http.post<{ detail: string }>(`${API_BASE_URL}/auth/logout/`, { refresh }).pipe(
      finalize(() => this.clearSession()),
    );
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('johntv_access');
  }

  private persistSession(response: AuthResponse): void {
    localStorage.setItem('johntv_access', response.access);
    localStorage.setItem('johntv_refresh', response.refresh);
    localStorage.setItem('johntv_user', JSON.stringify(response.user));
    this.currentUserSignal.set(response.user);
  }

  private clearSession(): void {
    localStorage.removeItem('johntv_access');
    localStorage.removeItem('johntv_refresh');
    localStorage.removeItem('johntv_user');
    this.currentUserSignal.set(null);
  }

  private readUser(): User | null {
    const raw = localStorage.getItem('johntv_user');
    return raw ? (JSON.parse(raw) as User) : null;
  }
}
