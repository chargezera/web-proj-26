import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ErrorMessageService {
  extract(error: unknown): string {
    if (error instanceof HttpErrorResponse) {
      const payload = error.error;

      if (typeof payload === 'string') {
        return payload;
      }

      if (payload?.detail) {
        return payload.detail;
      }

      if (payload && typeof payload === 'object') {
        const joined = Object.entries(payload)
          .map(([field, value]) => `${field}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join(' | ');

        if (joined) {
          return joined;
        }
      }

      return `Request failed with status ${error.status}.`;
    }

    if (error instanceof Error) {
      return error.message;
    }

    return 'Something went wrong.';
  }
}
