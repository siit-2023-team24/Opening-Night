import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SubscriptionsComponent } from './subs/subscriptions/subscriptions.component';
import { UploadComponent } from './film/upload/upload.component';
import { UpdateComponent } from './film/update/update.component';
import { FilmPageComponent } from './film/film-page/film-page.component';
import { HomePageComponent } from './film/home-page/home-page.component';

const routes: Routes = [
  {component: SubscriptionsComponent, path: "subs"},
  {component: UploadComponent, path: "upload"},
  {component: UpdateComponent, path: "update/:id"},
  {component: FilmPageComponent, path: "film/:id"},
  {component: HomePageComponent, path: "home"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
