import { MatchMap } from './match-map.model';
import { Team } from './team.model';
import { Tournament } from './tournament.model';

export interface Match {
  id: number;
  title: string;
  tournament: Tournament;
  team_one: Team;
  team_two: Team;
  winner: Team | null;
  match_time: string;
  best_of: number;
  status: 'upcoming' | 'live' | 'finished';
  maps?: MatchMap[];
}
