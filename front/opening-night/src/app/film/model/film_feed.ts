export interface FilmFeedDTO {
    filmId: string,
    title: string,
    actors: string[],
    directors: string[],
    genres: string[],
    isSeries: boolean,
    series?: string,
    season?: number,
    episode?: number,
    username?: string
}