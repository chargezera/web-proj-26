export interface Post {
  id: number;
  author: number;
  author_username: string;
  match: number;
  match_title: string;
  title: string;
  body: string;
  confidence: number;
  created_at: string;
  updated_at: string;
}
