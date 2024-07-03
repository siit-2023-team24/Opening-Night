import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from './navbar/navbar.component';
import { HeaderComponent } from './header/header.component';
import { RouterModule } from "@angular/router";
import { MaterialModule } from '../material/material.module';


@NgModule({
  declarations: [
    NavbarComponent,
    HeaderComponent
  ],
  imports: [
    RouterModule,
    CommonModule,
    MaterialModule
  ],
  exports: [
    NavbarComponent,
    HeaderComponent
  ]
})
export class LayoutModule { }
