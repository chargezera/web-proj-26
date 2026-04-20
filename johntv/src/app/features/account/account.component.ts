import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

import { Post } from '../../models/post.model';
import { AuthService } from '../../services/auth.service';
import { ErrorMessageService } from '../../services/error-message.service';
import { PostsService } from '../../services/posts.service';

@Component({
  selector: 'app-account',
  imports: [CommonModule, RouterLink],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css',
})
export class AccountComponent implements OnInit {
  posts: Post[] = [];
  loading = true;
  errorMessage = '';

  constructor(
    public authService: AuthService,
    private postsService: PostsService,
    private errorMessageService: ErrorMessageService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
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
}
