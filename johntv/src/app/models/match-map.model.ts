import { Team } from './team.model';

export interface MatchMap {
  id: number;
  name: string;
  order: number;
  picked_by: Team | null;
  note: string;
}
