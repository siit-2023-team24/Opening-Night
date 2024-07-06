export interface UploadFilmDTO {
    id?: number,
    fileName: string,
    file: string,
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