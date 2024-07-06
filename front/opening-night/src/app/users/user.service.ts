import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from "rxjs"
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from "../../env/env";
import { User } from '../shared/user';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  private headers = new HttpHeaders({
    'Content-Type': 'application/json',
    skip: 'true',
  });

  user$ = new BehaviorSubject("");
  userState = this.user$.asObservable();

  constructor(private httpClient: HttpClient) { }

  register(user: User): Observable<Object> {
    return this.httpClient.post<User>(environment.apiHost + '/register', user);
  }

}
