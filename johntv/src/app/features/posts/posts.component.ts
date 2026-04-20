import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Match } from '../../models/match.model';
import { Post } from '../../models/post.model';
import { ErrorMessageService } from '../../services/error-message.service';
import { MatchesService } from '../../services/matches.service';
import { PostsService } from '../../services/posts.service';

@Component({
  selector: 'app-posts',
  imports: [CommonModule, FormsModule],
  templateUrl: './posts.component.html',
  styleUrl: './posts.component.css',
})
export class PostsComponent implements OnInit {
  matches: Match[] = [];
  posts: Post[] = [];
  form = {
    match: '',
    title: '',
    body: '',
    confidence: 70,
  };
  editingPostId: number | null = null;
  errorMessage = '';
  successMessage = '';
  loading = true;

  constructor(
    private matchesService: MatchesService,
    private postsService: PostsService,
    private errorMessageService: ErrorMessageService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loadMatches();
    this.loadPosts();
  }

  loadMatches(): void {
    this.matchesService.getMatches().subscribe({
      next: (matches) => {
        this.matches = matches;
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.errorMessage = this.errorMessageService.extract(error);
        this.cdr.detectChanges();
      },
    });
  }

  loadPosts(): void {
    this.loading = true;
    this.postsService.getPosts(true).subscribe({
      next: (posts) => {
        this.posts = posts;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.errorMessage = this.errorMessageService.extract(error);
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }

  submitPost(): void {
    this.errorMessage = '';
    this.successMessage = '';

    const payload = {
      match: Number(this.form.match),
      title: this.form.title,
      body: this.form.body,
      confidence: Number(this.form.confidence),
    };

    const request = this.editingPostId
      ? this.postsService.updatePost(this.editingPostId, payload)
      : this.postsService.createPost(payload);

    request.subscribe({
      next: () => {
        this.successMessage = this.editingPostId ? 'Post updated.' : 'Post published.';
        this.resetForm();
        this.loadPosts();
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.errorMessage = this.errorMessageService.extract(error);
        this.cdr.detectChanges();
      },
    });
  }

  startEdit(post: Post): void {
    this.editingPostId = post.id;
    this.form = {
      match: String(post.match),
      title: post.title,
      body: post.body,
      confidence: post.confidence,
    };
    this.successMessage = '';
  }

  removePost(postId: number): void {
    this.errorMessage = '';
    this.successMessage = '';
    this.postsService.deletePost(postId).subscribe({
      next: () => {
        this.successMessage = 'Post deleted.';
        if (this.editingPostId === postId) {
          this.resetForm();
        }
        this.loadPosts();
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.errorMessage = this.errorMessageService.extract(error);
        this.cdr.detectChanges();
      },
    });
  }

  resetForm(): void {
    this.editingPostId = null;
    this.form = {
      match: '',
      title: '',
      body: '',
      confidence: 70,
    };
  }
}
