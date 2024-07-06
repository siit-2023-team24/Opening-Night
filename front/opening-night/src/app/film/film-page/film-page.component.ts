import { Component, ElementRef, ViewChild } from '@angular/core';
import { UploadFilmDTO } from '../model/upload-film';
import { FilmService } from '../film.service';
import { ActivatedRoute } from '@angular/router';
import { SeriesEpisodeDTO } from '../model/series-episode';

@Component({
  selector: 'app-film-page',
  templateUrl: './film-page.component.html',
  styleUrls: ['./film-page.component.css']
})
export class FilmPageComponent {

  filmDTO: UploadFilmDTO = {
    fileName: '',
    title: '',
    description: '',
    actors: [],
    directors: [],
    genres: [],
    isSeries: false,
    file: ''
  };

  filmFile: File | undefined;
  filmId: number = 0; //TODO: dobijace id iz roditeljske komponente tj. str koja prikazuje sve filmove
  seasons: number[] = []
  episodes: SeriesEpisodeDTO[] = []

  @ViewChild('videoPlayer') videoPlayer: ElementRef<HTMLVideoElement> | undefined;
  videoSource: string | ArrayBuffer | null = null;

  constructor(
    private filmService: FilmService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    // Fetch the film ID from route params
    this.route.params.subscribe(params => {
      this.filmId = params['id'];
      this.fetchFilmData();
    });
  }

  fetchFilmData(): void {
    // this.filmService.getFilmById(this.filmId).subscribe(response => {
    //   this.filmDTO = response;
    //   if (this.filmDTO.isSeries && this.filmDTO.series) {
    //     this.getSeriesSeasons(this.filmDTO.series);
    //   }
    // }, error => {
    //   console.log('Error fetching film data', error);
    // });

    this.filmDTO = {
      id: this.filmId,
      fileName: 'asdfasdf',
      title: 'fasdfasdfas',
      description: 'fadsfasdfasd',
      actors: ['Christian Bale', 'Hugh Jackman', 'Emma Stone'],
      directors: ['Poopy Pooppants'],
      genres: ['comedy'],
      isSeries: false,
      series: 'Naruto',
      season: 4,
      episode: 1,
      file: 'sadasdadasd'
    };

    if(this.filmDTO.isSeries && this.filmDTO.series) {
      this.getSeriesEpisodes(this.filmDTO.series);
    }
  }

  getSeriesEpisodes(seriesName: string) {
    this.filmService.getEpisodesBySeries(this.filmDTO.series).subscribe(response => {
      this.episodes = response;
    }, error => {
      console.log('Error fetching film data', error);
    });

    this.episodes.forEach(ep => {
      if(!this.seasons.includes(ep.seasonNumber))
        this.seasons.push(ep.seasonNumber);
    });

    this.seasons.sort((a, b) => a - b);
    
    // this.episodes = [{ id: 1, seasonNumber: 1, episodeNumber: 10 },
    //                  { id: 2, seasonNumber: 2, episodeNumber: 10 },
    //                  { id: 3, seasonNumber: 3, episodeNumber: 10 },
    //                  { id: 4, seasonNumber: 4, episodeNumber: 10 },
    //                  { id: 5, seasonNumber: 5, episodeNumber: 10 },
    //                  { id: 6, seasonNumber: 6, episodeNumber: 10 },
    //                  { id: 7, seasonNumber: 7, episodeNumber: 7 }]
  }

  loadEpisode(id: number): void {
    this.filmService.getFilmById(id).subscribe(response => {
      this.filmDTO = response;
    }, error => {
      console.log('Error fetching episode data', error);
    });
  }
  
  onFileChange(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length) {
      this.filmFile = inputElement.files[0];
      this.filmDTO.fileName = this.filmFile.name;
      this.convertFileToBase64(this.filmFile)
    } 
    console.log(this.filmFile);
  }

  convertFileToBase64(file: File): void {
    const reader = new FileReader();
    reader.onload = () => {
      this.filmDTO.file = reader.result as string;
      this.videoSource = this.filmDTO.file;
      if(this.videoPlayer) {
        const video: HTMLVideoElement = this.videoPlayer.nativeElement;
        video.load();
      }
    };
    reader.readAsDataURL(file);
  }

  convertBase64ToVideo(): void {
    if (this.filmDTO.file) {
      this.videoSource = this.filmDTO.file;
    }
  }

}
