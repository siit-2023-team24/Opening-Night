import { Component } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  role: string = "USER";
  username: string = "";
  constructor(private router: Router) {
  }


  ngOnInit(): void {

    // if (this.authService.isLoggedIn()) {
    // }
    // else {
    //   this.role = 'NO_USER';
    // }

    // this.router.events.pipe(
    //   filter((event: Event): event is NavigationEnd => event instanceof NavigationEnd)
    // ).subscribe((event: NavigationEnd) => {
    //   this.ngOnInit();
    // });
  }

  logout() {
    // localStorage.removeItem('user');
    // this.router.navigate(['login']);

  }
}
