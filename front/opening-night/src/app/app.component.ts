import { Component } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Opening Night';
  private routeSubscription: Subscription;

  
  constructor(private router: Router, private activatedRoute: ActivatedRoute) {
    this.routeSubscription = this.router.events.subscribe((event)=> {
      if (event instanceof NavigationEnd) {
        this.title = this.activatedRoute.snapshot.firstChild?.queryParamMap.get('title') || 'Opening Night';
      }
    });
  }

  ngOnDestroy(): void {
    this.routeSubscription.unsubscribe();
  }

}
