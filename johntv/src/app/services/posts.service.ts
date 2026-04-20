import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../core/api.config';
import { Post } from '../models/post.model';

@Injectable({
  providedIn: 'root',
})
export class PostsService {
  constructor(private http: HttpClient) {}

  getPosts(mine = false): Observable<Post[]> {
    const params = mine ? new HttpParams().set('mine', 'true') : undefined;
    return this.http.get<Post[]>(`${API_BASE_URL}/posts/`, { params });
  }

  createPost(payload: { match: number; title: string; body: string; confidence: number }): Observable<Post> {
    return this.http.post<Post>(`${API_BASE_URL}/posts/`, payload);
  }

  updatePost(postId: number, payload: { match: number; title: string; body: string; confidence: number }): Observable<Post> {
    return this.http.put<Post>(`${API_BASE_URL}/posts/${postId}/`, payload);
  }

  deletePost(postId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE_URL}/posts/${postId}/`);
  }
}
