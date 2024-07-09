import { Component, OnInit } from '@angular/core';
import { UploadFilmDTO } from '../model/upload-film';
import { ENTER, COMMA } from '@angular/cdk/keycodes';
import { FilmService } from '../film.service';
import { ActivatedRoute } from '@angular/router';
import { Genre } from 'src/app/shared/genre';
import { ActorsAndDirectorsDTO } from 'src/app/shared/actorsAndDirectors';

@Component({
  selector: 'app-update',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css']
})
export class UpdateComponent implements OnInit{

  filmDTO: UploadFilmDTO = {
    fileName: '',
    title: '',
    description: '',
    actors: [],
    directors: [],
    genres: [],
    isSeries: false,
    fileContent: ''
  };

  selectedFile: File | undefined;
  seriesList: string[] = []; //'One piece', 'Naruto', 'Fuji'];

  actors: string[] = [];
  //   'Matt Damon', 'Leo Dicaprio', 'Jack Nicholson', 'Meryl Streep', 'Tom Hanks', 
  //   'Robert De Niro', 'Al Pacino', 'Angelina Jolie', 'Brad Pitt', 'Johnny Depp', 
  //   'Morgan Freeman', 'Scarlett Johansson', 'Natalie Portman', 'Jennifer Lawrence', 
  //   'Denzel Washington', 'Christian Bale', 'Hugh Jackman', 'Emma Stone', 'Ryan Gosling', 
  //   'Charlize Theron'
  // ];
  directors: string[] = [] //'Poopy Pooppants', 'Milica Misic', 'Konjic'];
  genres = Object.values(Genre)
  newActor = '';
  newDirector = '';
  newSeries = '';
  filmId: string = ''; //TODO: dobijace id iz roditeljske komponente tj. str koja prikazuje sve filmove ili str jednog filma
  hasFileChanged: boolean = false

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

    this.getSeriesList();
  }

  fetchFilmData(): void {
    this.filmService.getFilmById(this.filmId).subscribe(response => {
      this.filmDTO = response;
    }, error => {
      console.log('Error fetching film data', error);
    });

    // this.filmDTO = {
    //   id: this.filmId,
    //   fileName: 'asdfasdf',
    //   title: 'fasdfasdfas',
    //   description: 'fadsfasdfasd',
    //   actors: ['Christian Bale', 'Hugh Jackman', 'Emma Stone'],
    //   directors: ['Poopy Pooppants'],
    //   genres: ['comedy'],
    //   isSeries: true,
    //   series: 'Naruto',
    //   season: 4,
    //   episode: 1,
    //   file: 'sadasdadasd'
    // };
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
      this.filmDTO.series = '';
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
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length) {
      this.selectedFile = inputElement.files[0];
      this.filmDTO.fileName = this.selectedFile.name;
      this.convertFileToBase64(this.selectedFile)
    } 
    console.log(this.selectedFile);
  }

  convertFileToBase64(file: File): void {
    const reader = new FileReader();
    reader.onload = () => {
      this.filmDTO.fileContent = reader.result as string;
    };
    reader.readAsDataURL(file);
  }

  addNewActor(): void {
    if (this.newActor && !this.actors.includes(this.newActor)) {
      this.actors.push(this.newActor);
      this.filmDTO.actors.push(this.newActor);
      this.newActor = '';
    }
  }

  addNewDirector(): void {
    if (this.newDirector && !this.directors.includes(this.newDirector)) {
      this.directors.push(this.newDirector);
      this.filmDTO.directors.push(this.newDirector);
      this.newDirector = '';
    }
  }

  addNewSeries(): void {
    if (this.newSeries && !this.seriesList.includes(this.newSeries)) {
      this.seriesList.push(this.newSeries);
      this.filmDTO.series = this.newSeries;
      this.newSeries = '';
    }
  }

  onSubmit() {
    if(this.hasFileChanged) {
      // this.filmService.updateFileChanged(this.filmDTO).subscribe(response => {
      //   console.log('Update successful', response);
      // }, error => {
      //   console.log('Update failed', error);
      // });
      console.log(this.filmDTO)
    } else {
      // this.filmService.update(this.filmDTO).subscribe(response => {
      //   console.log('Update successful', response);
      // }, error => {
      //   console.log('Update failed', error);
      // });
      console.log(this.filmDTO)
    }
  }

}
