import { Component, OnInit } from '@angular/core';
import { FilmCardDTO } from '../model/film-card';
import { FilmService } from '../film.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{

  films: FilmCardDTO[] = [];
  searchTerm: string = '';

  constructor(private filmService: FilmService, private router: Router) { }

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

  search(): void {}

}
