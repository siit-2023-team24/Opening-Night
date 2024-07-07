import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ValidatorFn, ValidationErrors, AbstractControl} from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../user.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { User } from '../model/user';

const passwordMatchValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const passwordControl = control.get('password');
  const confirmPasswordControl = control.get('confirmPassword');

  if (passwordControl && confirmPasswordControl && passwordControl.value !== confirmPasswordControl.value) {
    if (confirmPasswordControl.errors) {
      confirmPasswordControl.setErrors({ ...confirmPasswordControl.errors, passwordMismatch: true });
    } else {
      confirmPasswordControl.setErrors({ passwordMismatch: true });
    }
    return { passwordMismatch: true };
  } else {
    if (confirmPasswordControl) {
      confirmPasswordControl.setErrors(null);
    }
    return null;
  }
};

export function passwordPolicyValidator(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any } | null => {
    const value = control.value;
    if (!value) {
      return null;
    }

    const minLength = 8;
    if (value.length < minLength) return { error: `Password must contain a minimum length of ${minLength} characters` };
    if (!/[a-z]/.test(value)) return { error: 'Password must contain at least one lowercase letter' };
    if (!/[A-Z]/.test(value)) return { error: 'Password must contain at least one uppercase letter' };
    if (!/\d/.test(value)) return { error: 'Password must contain at least one digit' };
    if (!/[\-_!@#$%^&*(),.?":{}|<>]/.test(value)) return { error: 'At least one special character' };
    return null
  };
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css', '../../../styles.css']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  errorMessage: string = '';

  constructor(private formBuilder: FormBuilder, private router: Router, private userService: UserService, 
    private snackBar: MatSnackBar) {  }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(1)]],
      lastName: ['', [Validators.required, Validators.minLength(1)]],
      username: ['', Validators.required], // add format
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, passwordPolicyValidator()]], // add conditions
      confirmPassword: ['', [Validators.required, Validators.minLength(8)]], // add conditions
      birthdayDate: ['', Validators.required]
    }, { validator: passwordMatchValidator });
  }

  isOver18(birthday: Date, now: Date): boolean {
    console.log(birthday)
    const yearNow = now.getFullYear();
    const yearBirthday = birthday.getFullYear();
    const monthNow = now.getMonth();
    const monthBirthday = birthday.getMonth();
    const dayNow = now.getDate();
    const dayBirthday = birthday.getDate();
  
    const yearDifference = yearNow - yearBirthday;
  
    if (yearDifference < 18) {
      return false;
    }
    if (yearDifference > 18) {
      return true;
    }
    return (monthNow > monthBirthday || (monthNow === monthBirthday && dayNow >= dayBirthday))
  }

  formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2); // months are 0-based
    const day = ('0' + date.getDate()).slice(-2);
  
    return `${year}-${month}-${day}`;
  }

  onRegisterClick(): void {
    if(!this.registerForm.valid) {
      this.errorMessage = 'Please fill out all the fields according to the validations.'
      return;
    }
    this.errorMessage = ''
    if(!this.isOver18(this.registerForm.value.birthdayDate, new Date())) {
      this.errorMessage = 'You must be at least 18 years old to register.'
      return;
    }
    this.register();
  }

  register(): void {
    this.errorMessage = '';
    let user: User = this.registerForm.value;
    user.birthday = this.formatDate(this.registerForm.value.birthdayDate)
    user.isGuest = true
    console.log(user)
    this.userService.register(user).subscribe({
      next: (response: Object) => {
          console.log("SUCCESS! " + user);
          console.log(response)
          this.router.navigate(['login']);
          this.snackBar.open('Registration successful!', 'Close', {
            duration: 3000,
            verticalPosition: 'top',
            horizontalPosition: 'center'
          });
        }
      ,
      error: (error) => {
        if (error.error) {
          this.errorMessage = error.error;
        } else {
          this.errorMessage = 'An unexpected error occurred. Please try again.';
        }
      }
    });
  }
}


