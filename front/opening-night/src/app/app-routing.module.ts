import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SubscriptionsComponent } from './subs/subscriptions/subscriptions.component';
import { UploadComponent } from './film/upload/upload.component';
import { UpdateComponent } from './film/update/update.component';
import { FilmPageComponent } from './film/film-page/film-page.component';
import { HomePageComponent } from './film/home-page/home-page.component';
import { FeedComponent } from './film/feed/feed.component';
import { RegisterComponent } from './users/register/register.component';
import { LoginComponent } from './users/login/login.component';
import { AuthGuard } from './auth/guard';

const routes: Routes = [
  {component: SubscriptionsComponent, path: "subs", canActivate: [AuthGuard], data : {role: ['viewer']}},
  {component: UploadComponent, path: "upload", canActivate: [AuthGuard], data : {role: ['admin']}},
  {component: UpdateComponent, path: "update/:id", canActivate: [AuthGuard], data : {role: ['admin']}},
  {component: FilmPageComponent, path: "film/:id", canActivate: [AuthGuard], data : {role: ['viewer', 'admin']}},
  {component: HomePageComponent, path: "home"},
  {component: FeedComponent, path: "feed", canActivate: [AuthGuard], data : {role: ['viewer']}},
  {component: RegisterComponent, path: "register", canActivate: [AuthGuard], data : {role: ['none']}},
  {component: LoginComponent, path: "login", canActivate: [AuthGuard], data : {role: ['none']}},
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', redirectTo: 'home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
