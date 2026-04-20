import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { Match } from '../../models/match.model';
import { ErrorMessageService } from '../../services/error-message.service';
import { MatchesService } from '../../services/matches.service';

@Component({
  selector: 'app-match-detail',
  imports: [CommonModule, RouterLink],
  templateUrl: './match-detail.component.html',
  styleUrl: './match-detail.component.css',
})
export class MatchDetailComponent implements OnInit {
  match: Match | null = null;
  loading = true;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private matchesService: MatchesService,
    private errorMessageService: ErrorMessageService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    const matchId = Number(this.route.snapshot.paramMap.get('id'));

    if (!matchId) {
      this.errorMessage = 'Match not found.';
      this.loading = false;
      this.cdr.detectChanges();
      return;
    }

    this.matchesService.getMatch(matchId).subscribe({
      next: (match) => {
        this.match = match;
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
