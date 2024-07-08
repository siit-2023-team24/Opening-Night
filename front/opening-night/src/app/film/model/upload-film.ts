export interface UploadFilmDTO {
    filmId?: string,
    fileName: string,
    fileContent: string,
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