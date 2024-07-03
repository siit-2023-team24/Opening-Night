import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/env/env';
import { SubscriptionDTO } from './model/subscription';

@Injectable({
  providedIn: 'root'
})
export class SubsService {

  constructor(private httpClient: HttpClient) { }

  get(username: string): Observable<SubscriptionDTO> {
    return this.httpClient.get<SubscriptionDTO>(environment.apiHost + '/subscriptions/' + username);
  }

  update(username: string, subs: SubscriptionDTO): Observable<string> {
    return this.httpClient.post<string>(environment.apiHost + '/subscriptions/' + username, subs);
  }
}
