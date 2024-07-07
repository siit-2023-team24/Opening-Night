export interface Rating {
    filmId?: string;
    username: string;
    timestamp?: string;
    stars: number;
    genres?: string[],
    directors?: string[],
    actors?: string[]
}