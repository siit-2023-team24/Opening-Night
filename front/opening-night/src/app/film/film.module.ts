import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FilmComponent } from './film/film.component';
import { RatingsComponent } from './ratings/ratings.component';
import { MaterialModule } from '../material/material.module';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { SharedModule } from '../shared/shared.module';
import { RatingCardComponent } from './rating-card/rating-card.component';



@NgModule({
  declarations: [
    FilmComponent,
    RatingsComponent,
    RatingCardComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule,
    SharedModule,
    FormsModule
  ],
  exports: [
    FilmComponent,
    RatingsComponent
  ]
})
export class FilmModule { }
