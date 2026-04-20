import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../core/api.config';
import { Match } from '../models/match.model';
import { Team } from '../models/team.model';
import { Tournament } from '../models/tournament.model';

@Injectable({
  providedIn: 'root',
})
export class MatchesService {
  constructor(private http: HttpClient) {}

  getMatches(filters?: { team?: string; search?: string; status?: string }): Observable<Match[]> {
    let params = new HttpParams();

    if (filters?.team) {
      params = params.set('team', filters.team);
    }
    if (filters?.search) {
      params = params.set('search', filters.search);
    }
    if (filters?.status) {
      params = params.set('status', filters.status);
    }

    return this.http.get<Match[]>(`${API_BASE_URL}/matches/`, { params });
  }

  getMatch(matchId: number): Observable<Match> {
    return this.http.get<Match>(`${API_BASE_URL}/matches/${matchId}/`);
  }

  getTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${API_BASE_URL}/teams/`);
  }

  getTournaments(): Observable<Tournament[]> {
    return this.http.get<Tournament[]>(`${API_BASE_URL}/tournaments/`);
  }
}
