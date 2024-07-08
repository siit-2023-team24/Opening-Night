export interface FilmCardDTO {
    filmId: string,
    title: string,
    isSeries: boolean,
    series?: string,
    season?: number,
    episode?: number
}