import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Account } from '../model/account';
import { User } from '../model/user';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css', '../../../styles.css']
})
export class LoginComponent {
  loginForm : FormGroup;
  errorMessage : string = '';

  constructor(private formBuilder : FormBuilder, private userService: UserService, private router: Router) {
    this.loginForm = this.formBuilder.group({
      username : ['', Validators.required],
      password : ['', Validators.required]
    })
  }

  login(): void {
    if(!this.loginForm.valid) {
      this.errorMessage = 'Please fill out both fields according to the validations.'
      return;
    }
    this.errorMessage = '';
    const account : Account = this.loginForm.value;

    this.userService.login(account).subscribe({
      next: (response: User) => {
        // localStorage.setItem('user', response.accessToken);
        // this.socketService.openSocket();
        
        // const helper = new JwtHelperService();
        // console.log(helper.decodeToken(response.accessToken));
        
        this.router.navigate(['home'])
        console.log("Success!")
      },
      error: (error) => {
        console.error('Login error:', error.error);
        this.errorMessage = error.error;
      }
    });
  }
}
