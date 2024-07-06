import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Rating } from './model/rating';
import { environment } from 'src/env/env';
import { Observable } from 'rxjs';
import { MessageResponse } from 'src/env/error-response';

@Injectable({
  providedIn: 'root'
})
export class RatingService {

  constructor(private httpClient: HttpClient) { }

  get(filmId: string): Observable<Rating[]> {
    return this.httpClient.get<Rating[]>(environment.apiHost + '/ratings/' + filmId);
  }

  rate(rating: Rating): Observable<MessageResponse> {
    return this.httpClient.post<MessageResponse>(environment.apiHost + '/ratings', rating);
  }


}
