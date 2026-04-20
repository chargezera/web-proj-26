import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { Match } from '../../models/match.model';
import { Team } from '../../models/team.model';
import { ErrorMessageService } from '../../services/error-message.service';
import { MatchesService } from '../../services/matches.service';

@Component({
  selector: 'app-matches',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './matches.component.html',
  styleUrl: './matches.component.css',
})
export class MatchesComponent implements OnInit {
  matches: Match[] = [];
  teams: Team[] = [];
  search = '';
  team = '';
  status = '';
  matchesError = '';
  teamsError = '';
  matchesLoading = true;
  teamsLoading = true;

  constructor(
    private matchesService: MatchesService,
    private errorMessageService: ErrorMessageService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loadTeams();
    this.loadMatches();
  }

  loadTeams(): void {
    this.matchesService.getTeams().subscribe({
      next: (teams) => {
        this.teams = teams;
        this.teamsLoading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.teamsError = this.errorMessageService.extract(error);
        this.teamsLoading = false;
        this.cdr.detectChanges();
      },
    });
  }

  loadMatches(): void {
    this.matchesLoading = true;
    this.matchesError = '';
    this.matchesService
      .getMatches({
        team: this.team,
        search: this.search,
        status: this.status,
      })
      .subscribe({
        next: (matches) => {
          this.matches = matches;
          this.matchesLoading = false;
          this.cdr.detectChanges();
        },
        error: (error) => {
          this.matchesError = this.errorMessageService.extract(error);
          this.matchesLoading = false;
          this.cdr.detectChanges();
        },
      });
  }

  clearFilters(): void {
    this.search = '';
    this.team = '';
    this.status = '';
    this.loadMatches();
  }
}
