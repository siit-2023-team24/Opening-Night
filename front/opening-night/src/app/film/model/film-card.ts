export interface FilmCardDTO {
    id: number,
    title: string,
    isSeries: boolean,
    series?: string,
    season?: number,
    episode?: number
}