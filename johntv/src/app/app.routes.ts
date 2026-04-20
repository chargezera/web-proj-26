import { Routes } from '@angular/router';

import { authGuard } from './core/auth.guard';
import { AccountComponent } from './features/account/account.component';
import { AuthComponent } from './features/auth/auth.component';
import { HomeComponent } from './features/home/home.component';
import { MatchDetailComponent } from './features/match-detail/match-detail.component';
import { MatchesComponent } from './features/matches/matches.component';
import { PostsComponent } from './features/posts/posts.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'matches',
    component: MatchesComponent,
  },
  {
    path: 'matches/:id',
    component: MatchDetailComponent,
  },
  {
    path: 'posts',
    component: PostsComponent,
    canActivate: [authGuard],
  },
  {
    path: 'account',
    component: AccountComponent,
    canActivate: [authGuard],
  },
  {
    path: 'auth',
    component: AuthComponent,
  },
  {
    path: '**',
    redirectTo: '',
  },
];
