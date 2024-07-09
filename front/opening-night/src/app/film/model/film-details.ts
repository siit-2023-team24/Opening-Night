export interface FilmDetailsDTO {
    filmId: string,
    fileName: string,
    fileContentOriginal: string,
    fileContent360p: string,
    fileContent144p: string,
    title: string,
    description: string,
    actors: string[],
    directors: string[],
    genres: string[],
    isSeries: boolean,
    series?: string,
    season?: number,
    episode?: number
}