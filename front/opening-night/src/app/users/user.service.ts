import { Injectable } from '@angular/core';
import { Observable } from "rxjs"
import { HttpClient } from '@angular/common/http';
import { environment } from "../../env/env";
import { User } from './model/user';
import { Account } from './model/account';
import { Tokens } from './model/tokens';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  constructor(private httpClient: HttpClient) { }

  register(user: User): Observable<Object> {
    return this.httpClient.post<User>(environment.apiHost + '/register', user);
  }

  login(account: Account): Observable<Tokens> {
    return this.httpClient.post<Tokens>(environment.apiHost + '/login', account);
  }

}
