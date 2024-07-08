import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/env/env';
import { UploadFilmDTO } from './model/upload-film';
import { ActorsAndDirectorsDTO } from '../shared/actorsAndDirectors';
import { SeriesEpisodeDTO } from './model/series-episode';
import { FilmCardDTO } from './model/film-card';
import { FilmFeedDTO } from './model/film_feed';
import { MessageResponse } from 'src/env/error-response';

@Injectable({
  providedIn: 'root'
})
export class FilmService {

  constructor(private http: HttpClient) { }

  getSeriesList(): Observable<string[]> {
    return this.http.get<string[]>(environment.apiHost + '/films/series');
  }

  upload(filmDTO: UploadFilmDTO): Observable<UploadFilmDTO> {
    return this.http.post<UploadFilmDTO>(environment.apiHost + '/films', filmDTO);
  }

  getFilmById(id: number): Observable<UploadFilmDTO> {
    return this.http.get<UploadFilmDTO>(environment.apiHost + '/films/' + id);
  }

  updateFileChanged(filmDTO: UploadFilmDTO): Observable<UploadFilmDTO> {
    return this.http.put<UploadFilmDTO>(environment.apiHost + '/films/update', filmDTO);
  }

  update(filmDTO: UploadFilmDTO): Observable<UploadFilmDTO> {
    return this.http.put<UploadFilmDTO>(environment.apiHost + '/films', filmDTO);
  }

  getActorsAndDirectors(): Observable<ActorsAndDirectorsDTO> {
    return this.http.get<ActorsAndDirectorsDTO>(environment.apiHost + '/actors-and-directors')
  }

  getEpisodesBySeries(seriesName: string | undefined): Observable<SeriesEpisodeDTO[]> {
    return this.http.get<SeriesEpisodeDTO[]>(environment.apiHost + '/series/' + seriesName + '/episodes')
  }

  getAllFilms(): Observable<FilmCardDTO[]> {
    return this.http.get<FilmCardDTO[]>(environment.apiHost + '/films');
  }

  getFeed(username: string): Observable<FilmFeedDTO[]> {
    return this.http.get<FilmFeedDTO[]>(environment.apiHost + '/feed/' + username);
  }

  search(input: string): Observable<FilmCardDTO[]> {
    return this.http.get<FilmCardDTO[]>(environment.apiHost + '/search/' + input)
  }

  delete(filmId: string): Observable<MessageResponse> {
    return this.http.delete<MessageResponse>(environment.apiHost + '/films/' + filmId)
  }
}
