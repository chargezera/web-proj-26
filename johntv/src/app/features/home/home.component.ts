import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

import { Match } from '../../models/match.model';
import { Team } from '../../models/team.model';
import { Tournament } from '../../models/tournament.model';
import { ErrorMessageService } from '../../services/error-message.service';
import { MatchesService } from '../../services/matches.service';

@Component({
  selector: 'app-home',
  imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent implements OnInit {
  matches: Match[] = [];
  teams: Team[] = [];
  tournaments: Tournament[] = [];
  matchesError = '';
  teamsError = '';
  tournamentsError = '';
  matchesLoading = true;
  teamsLoading = true;
  tournamentsLoading = true;

  constructor(
    private matchesService: MatchesService,
    private errorMessageService: ErrorMessageService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.matchesService.getMatches().subscribe({
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

    this.matchesService.getTournaments().subscribe({
      next: (tournaments) => {
        this.tournaments = tournaments;
        this.tournamentsLoading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.tournamentsError = this.errorMessageService.extract(error);
        this.tournamentsLoading = false;
        this.cdr.detectChanges();
      },
    });
  }
}
