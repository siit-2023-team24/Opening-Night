import { Component, OnInit } from '@angular/core';
import { UploadFilmDTO } from '../model/upload-film';
import { ENTER, COMMA } from '@angular/cdk/keycodes';
import { FilmService } from '../film.service';
import { ActivatedRoute } from '@angular/router';
import { Genre } from 'src/app/shared/genre';
import { ActorsAndDirectorsDTO } from 'src/app/shared/actorsAndDirectors';
import { FilmDetailsDTO } from '../model/film-details';
import { UpdateFilmDTO } from '../model/film-update';

@Component({
  selector: 'app-update',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css']
})
export class UpdateComponent implements OnInit{

  uploadFilmDTO: UploadFilmDTO = {
    fileName: '',
    title: '',
    description: '',
    actors: [],
    directors: [],
    genres: [],
    isSeries: false,
    fileContent: ''
  };

  updateFilmDTO: UpdateFilmDTO = {
    filmId: '',
    fileName: '',
    title: '',
    description: '',
    actors: [],
    directors: [],
    genres: [],
    isSeries: false
  }

  selectedFile: File | undefined;
  seriesList: string[] = [];

  actors: string[] = [];
  directors: string[] = [];
  genres = Object.values(Genre);
  newActor = '';
  newDirector = '';
  newSeries = '';
  filmId: string = '';
  hasFileChanged: boolean = false

  constructor(
    private filmService: FilmService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.filmId = params['id'];
      this.fetchFilmData();
    });

    this.getActorsAndDirectors();
    this.getSeriesList();
  }

  fetchFilmData(): void {
    this.filmService.getFilmByIdUpdate(this.filmId).subscribe(response => {
      this.updateFilmDTO = response;
      this.uploadFilmDTO = {
        filmId: this.updateFilmDTO.filmId,
        fileName: this.updateFilmDTO.fileName,
        title: this.updateFilmDTO.title,
        description: this.updateFilmDTO.description,
        actors: this.updateFilmDTO.actors,
        directors: this.updateFilmDTO.directors,
        genres: this.updateFilmDTO.genres,
        isSeries: this.updateFilmDTO.isSeries,
        series: this.updateFilmDTO.series,
        season: this.updateFilmDTO.season,
        episode: this.updateFilmDTO.episode,
        fileContent: ''
      }
    }, error => {
      console.log('Error fetching film data', error);
    });
  }

  getActorsAndDirectors() {
    this.filmService.getActorsAndDirectors().subscribe({
      next: (data: ActorsAndDirectorsDTO) => {
        this.directors = data.directors;
        this.directors.sort()
        this.actors = data.actors
        this.actors.sort()
      }
    })
  }

  onToggleSeries(event: any) {
    if (!event.target.checked) {
      this.uploadFilmDTO.series = '';
    }
  }
  getSeriesList() {
    this.filmService.getSeriesList().subscribe(response => {
      this.seriesList = response;
    }, error => {
      console.log('Error getting the series list', error);
    });
  }

  onFileChange(event: Event): void {
    this.hasFileChanged = true
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length) {
      this.selectedFile = inputElement.files[0];
      this.uploadFilmDTO.fileName = this.selectedFile.name;
      this.convertFileToBase64(this.selectedFile)
    }
  }

  convertFileToBase64(file: File): void {
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = (reader.result as string).split(',')[1]; // Remove the prefix
      this.uploadFilmDTO.fileContent = base64String;
    };
    reader.readAsDataURL(file);
  }

  addNewActor(): void {
    if (this.newActor && !this.actors.includes(this.newActor)) {
      this.actors.push(this.newActor);
      this.uploadFilmDTO.actors.push(this.newActor);
      this.newActor = '';
    }
  }

  addNewDirector(): void {
    if (this.newDirector && !this.directors.includes(this.newDirector)) {
      this.directors.push(this.newDirector);
      this.uploadFilmDTO.directors.push(this.newDirector);
      this.newDirector = '';
    }
  }

  addNewSeries(): void {
    if (this.newSeries && !this.seriesList.includes(this.newSeries)) {
      this.seriesList.push(this.newSeries);
      this.uploadFilmDTO.series = this.newSeries;
      this.newSeries = '';
    }
  }

  onSubmit() {
    if(this.hasFileChanged) {
      this.filmService.upload(this.uploadFilmDTO).subscribe(response => {
        console.log('Update with file successful', response);
      }, error => {
        console.log('Update with file failed', error);
      });
    } else {
      this.filmService.update(this.uploadFilmDTO).subscribe(response => {
        console.log('Update successful', response);
      }, error => {
        console.log('Update failed', error);
      });
    }
  }

}
