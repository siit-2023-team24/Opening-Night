import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/env/env';
import { UploadFilmDTO } from './model/upload-film';
import { ActorsAndDirectorsDTO } from '../shared/actorsAndDirectors';
import { SeriesEpisodeDTO } from './model/series-episode';
import { FilmCardDTO } from './model/film-card';
import { FilmFeedDTO } from './model/film_feed';
import { FilmDetailsDTO } from './model/film-details';
import { UpdateFilmDTO } from './model/film-update';

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

  getFilmById(id: string): Observable<FilmDetailsDTO> {
    return this.http.get<FilmDetailsDTO>(environment.apiHost + '/films/' + id);
  }

  getFilmByIdUpdate(id: string): Observable<UpdateFilmDTO> {
    return this.http.get<UpdateFilmDTO>(environment.apiHost + '/update/' + id);
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

}
