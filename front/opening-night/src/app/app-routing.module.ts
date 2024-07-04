import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SubscriptionsComponent } from './subs/subscriptions/subscriptions.component';
import { FilmComponent } from './film/film/film.component';

const routes: Routes = [
  {component: SubscriptionsComponent, path: "subs"},
  {component: FilmComponent, path: "film"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
