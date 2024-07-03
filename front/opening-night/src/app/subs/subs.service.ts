import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/env/env';
import { SubscriptionDTO } from './model/subscription';
import { MessageResponse } from 'src/env/error-response';

@Injectable({
  providedIn: 'root'
})
export class SubsService {

  constructor(private httpClient: HttpClient) { }

  get(username: string): Observable<SubscriptionDTO> {
    return this.httpClient.get<SubscriptionDTO>(environment.apiHost + '/subscriptions/' + username);
  }

  update(username: string, subs: SubscriptionDTO): Observable<MessageResponse> {
    return this.httpClient.post<MessageResponse>(environment.apiHost + '/subscriptions/' + username, subs);
  }
}
