import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from './upload/upload.component';
import { MaterialModule } from '../material/material.module';
import { HttpClientModule } from '@angular/common/http';
import { UpdateComponent } from './update/update.component';
import { FilmPageComponent } from './film-page/film-page.component';
import { HomePageComponent } from './home-page/home-page.component';
import { AppRoutingModule } from '../app-routing.module';
import { FilmComponent } from './film/film.component';
import { RatingsComponent } from './ratings/ratings.component';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';
import { RatingCardComponent } from './rating-card/rating-card.component';



@NgModule({
  declarations: [
    UploadComponent,
    UpdateComponent,
    FilmPageComponent,
    HomePageComponent,
    FilmComponent,
    RatingsComponent,
    RatingCardComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    RouterModule,
    ReactiveFormsModule,
    SharedModule
  ],
  exports: [
    FilmComponent,
    RatingsComponent
  ]
})
export class FilmModule { }
