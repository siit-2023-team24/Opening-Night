import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from './upload/upload.component';
import { MaterialModule } from '../material/material.module';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { UpdateComponent } from './update/update.component';
import { FilmPageComponent } from './film-page/film-page.component';
import { HomePageComponent } from './home-page/home-page.component';
import { AppRoutingModule } from '../app-routing.module';



@NgModule({
  declarations: [
    UploadComponent,
    UpdateComponent,
    FilmPageComponent,
    HomePageComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    HttpClientModule,
    FormsModule,
    MatSlideToggleModule,
    AppRoutingModule
  ]
})
export class FilmModule { }
