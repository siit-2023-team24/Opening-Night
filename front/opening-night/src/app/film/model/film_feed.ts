export interface FilmFeedDTO {
    id?: number,
    fileName: string,
    title: string,
    actors: string[],
    directors: string[],
    genres: string[],
    isSeries: boolean,
    series?: string,
    season?: number,
    episode?: number
}