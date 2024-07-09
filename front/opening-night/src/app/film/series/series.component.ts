import { Component, OnInit } from '@angular/core';
import { FilmService } from '../film.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { filter } from 'rxjs';
import { MessageResponse } from 'src/env/error-response';
import { AuthService } from 'src/app/auth/auth.service';
import { SeriesEpisodeDTO } from '../model/series-episode';

@Component({
  selector: 'app-series',
  templateUrl: './series.component.html',
  styleUrls: ['./series.component.css']
})
export class SeriesComponent implements OnInit{

  episodes: SeriesEpisodeDTO[] = [];
  searchTerm: string = '';
  seriesName: string = '';
  filterForm: FormGroup;

  constructor(private filmService: FilmService, private router: Router,
              private formBuilder: FormBuilder, private authService: AuthService,
              private route: ActivatedRoute) {
      this.filterForm = this.formBuilder.group({
        title: [null],
        genres: [null],
        directors: [null],
        actors: [null]
      })
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.seriesName = params['name'];
      this.fetchEpisodes();
    });
  }

  fetchEpisodes(): void {
    this.filmService.getEpisodesBySeries(this.seriesName).subscribe({
      next: (episodes: SeriesEpisodeDTO[]) => {
        this.episodes = episodes;
      },
      error: (error) => {
        console.error('Error fetching films:', error);
      }
    });
  }
}

