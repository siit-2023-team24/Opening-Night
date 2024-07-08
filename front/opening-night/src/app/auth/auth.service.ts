import { Injectable } from '@angular/core';
import { Tokens } from '../users/model/tokens';
import { JwtHelperService } from '@auth0/angular-jwt';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }
  helper: JwtHelperService = new JwtHelperService();

  login(tokens: Tokens) {
    localStorage.setItem('idToken', tokens.idToken);
    // localStorage.setItem('accessToken', tokens.accessToken);
    // localStorage.setItem('refreshToken', tokens.refreshToken);
  }

  getUsername(): string {
    if(!this.isLoggedIn()) return "";
    return this.helper.decodeToken(localStorage.getItem('idToken') || '')['cognito:username'];
  }

  getEmail(): string {
    if(!this.isLoggedIn()) return "";
    return this.helper.decodeToken(localStorage.getItem('idToken') || '')['email'];
  }

  getRole() : string {
    if(!this.isLoggedIn()) return "none";
    if (this.helper.decodeToken(localStorage.getItem('idToken') || '')['custom:is_viewer'] == "True") return "viewer";
    return "admin";
  }

  isLoggedIn(): boolean {
    return localStorage.getItem('idToken')!=null;
  }

  logout(): void {
    localStorage.removeItem('idToken');
  }

}
