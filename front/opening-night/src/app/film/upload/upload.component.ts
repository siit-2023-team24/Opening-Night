import { Component, OnInit } from '@angular/core';
import { FilmService } from '../film.service';
import { UploadFilmDTO } from '../model/upload-film';
import { ActorsAndDirectorsDTO } from 'src/app/shared/actorsAndDirectors';
import { Genre } from 'src/app/shared/genre';
import { Router } from '@angular/router';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {
  
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
  seriesList: string[] = [] //'One piece', 'Naruto', 'Fuji'];

  actors: string[] = []
  //   'Matt Damon', 'Leo Dicaprio', 'Jack Nicholson', 'Meryl Streep', 'Tom Hanks', 
  //   'Robert De Niro', 'Al Pacino', 'Angelina Jolie', 'Brad Pitt', 'Johnny Depp', 
  //   'Morgan Freeman', 'Scarlett Johansson', 'Natalie Portman', 'Jennifer Lawrence', 
  //   'Denzel Washington', 'Christian Bale', 'Hugh Jackman', 'Emma Stone', 'Ryan Gosling', 
  //   'Charlize Theron'
  // ];
  directors: string[] = [] // 'Poopy Pooppants', 'Milica Misic', 'Konjic'];
  genres = Object.values(Genre)
  newActor = '';
  newDirector = '';
  newSeries = '';

  constructor(private filmService: FilmService, private router: Router) {}

  ngOnInit(): void {
    this.getSeriesList();
    this.getActorsAndDirectors();
  }

  getActorsAndDirectors() {
    this.filmService.getActorsAndDirectors().subscribe({
      next: (data: ActorsAndDirectorsDTO) => {
        this.directors = data.directors;
        this.directors.sort()
        console.log("dir")
        console.log(this.directors)
        this.actors = data.actors
        this.actors.sort()
      }
    })
  }

  onToggleSeries(event: any) {
    if(!event.checked) {
      this.filmDTO.series = '';
    }
  }

  getSeriesList() {
    this.filmService.getSeriesList().subscribe(response => {
      this.seriesList = response;
      this.seriesList.sort();
    }, error => {
      console.log('Error getting the series list', error);
    });

    console.log(this.seriesList)
  }

  onFileChange(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length) {
      this.selectedFile = inputElement.files[0];
      this.filmDTO.fileName = this.selectedFile.name;
      this.convertFileToBase64(this.selectedFile);
    } 
    console.log(this.selectedFile);
  }

  convertFileToBase64(file: File): void {
    const reader = new FileReader();
    reader.onload = () => {
        const base64String = (reader.result as string).split(',')[1]; // Remove the prefix
        this.filmDTO.fileContent = base64String;
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
    // console.log(this.filmDTO)
    // console.log(this.filmDTO.series)
    // console.log(this.filmDTO.season)
    // console.log(this.filmDTO.episode)
    this.filmService.upload(this.filmDTO).subscribe({
      next: (response) => {
        console.log('Upload successful', response);
        this.router.navigate(['home']);
      },
      error: (error) => {
        console.log('Upload failed', error);
      }
    });
  }
}
