export interface ApiError {
  detail?: string;
  [key: string]: string | string[] | undefined;
}
