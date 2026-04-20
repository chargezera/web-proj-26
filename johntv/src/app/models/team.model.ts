import { Player } from './player.model';

export interface Team {
  id: number;
  name: string;
  country: string;
  world_ranking: number;
  logo_url: string;
  players?: Player[];
}
