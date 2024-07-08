import { Component } from '@angular/core';
import { Event, NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from 'src/app/auth/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css', "../../../styles.css"]
})
export class NavbarComponent {

  role: string = "none";
  username: string = "";
  constructor(private router: Router, private authService: AuthService) {
  }


  ngOnInit(): void {

    this.role = this.authService.getRole()

    this.router.events.pipe(
      filter((event: Event): event is NavigationEnd => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.ngOnInit();
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['login']);
  }
}
