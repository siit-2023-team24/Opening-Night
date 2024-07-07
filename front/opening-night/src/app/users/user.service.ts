import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from "rxjs"
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from "../../env/env";
import { User } from './model/user';
import { Account } from './model/account';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  constructor(private httpClient: HttpClient) { }

  register(user: User): Observable<Object> {
    return this.httpClient.post<User>(environment.apiHost + '/register', user);
  }

  login(account: Account): Observable<User> {
    return this.httpClient.post<User>(environment.apiHost + '/login', account);
  }

}
