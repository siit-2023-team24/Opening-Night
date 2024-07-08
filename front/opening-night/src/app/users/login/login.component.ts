import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Account } from '../model/account';
import { AuthService } from 'src/app/auth/auth.service';
import { Tokens } from '../model/tokens';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css', '../../../styles.css']
})
export class LoginComponent {
  loginForm : FormGroup;
  errorMessage : string = '';

  constructor(private formBuilder : FormBuilder, private userService: UserService, private router: Router, private authService: AuthService) {
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
      next: (response: Tokens) => {
        this.authService.login(response);
        console.log(this.authService.getUsername())
        this.router.navigate(['register'])
      },
      error: (error) => {
        console.error('Login error:', error.error);
        this.errorMessage = error.error;
      }
    });
  }
}
