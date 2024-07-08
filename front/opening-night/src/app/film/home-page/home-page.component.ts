import { Component, OnInit } from '@angular/core';
import { FilmCardDTO } from '../model/film-card';
import { FilmService } from '../film.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { filter } from 'rxjs';
import { MessageResponse } from 'src/env/error-response';
import { AuthService } from 'src/app/auth/auth.service';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{

  films: FilmCardDTO[] = [];
  searchTerm: string = '';

  filterForm: FormGroup;

  constructor(private filmService: FilmService, private router: Router,
              private formBuilder: FormBuilder, private authService: AuthService) {
      this.filterForm = this.formBuilder.group({
        title: [null],
        genres: [null],
        directors: [null],
        actors: [null]
      })
  }

  ngOnInit(): void {
    this.fetchFilms();
  }

  fetchFilms(): void {
    this.filmService.getAllFilms().subscribe(
      (films: FilmCardDTO[]) => {
        this.films = films;
      },
      error => {
        console.error('Error fetching films:', error);
      }
    );

    // const filmDTO = {
    //   id: 1,
    //   title: 'fasdfasdfas',
    //   isSeries: true,
    //   series: 'Naruto',
    //   season: 4,
    //   episode: 1
    // };

    // this.films.push(filmDTO);
  }

  search(): void {
    console.log(this.searchTerm);
    this.filmService.search(this.searchTerm).subscribe({
      next: (data: FilmCardDTO[]) => {
        this.films = data;
      },
      error: (error: MessageResponse) => {
        console.log(error.message);
      }
    });
  }


  filterSearch(): void {
    let data = this.filterForm.value;
    let input = data.title + '|' + data.genres + '|' + data.directors + '|' + data.actors;
    console.log(input);
    this.filmService.search(input).subscribe({
      next: (data: FilmCardDTO[]) => {
        this.films = data;
      },
      error: (error: MessageResponse) => {
        console.log(error.message);
      }
    });
  }
}

