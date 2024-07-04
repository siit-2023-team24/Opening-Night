import { Component, Input, OnInit } from '@angular/core';
import { RatingService } from '../rating.service';
import { Rating } from '../model/rating';
import { MessageResponse } from 'src/env/error-response';

@Component({
  selector: 'app-ratings',
  templateUrl: './ratings.component.html',
  styleUrls: ['./ratings.component.css']
})
export class RatingsComponent implements OnInit {

  @Input()
  filmId: string = '';

  stars: boolean[] = [false, false, false, false, false]
  rating: number = 0;
  noRating: boolean = false;

  ratings: Rating[] = [
    // {username: 'test', filmId: 'f123', timestamp: '12.12.1212.', stars: 4},
    // {username: 'test', filmId: 'f123', timestamp: '12.12.1212.', stars: 4},
    // {username: 'test', filmId: 'f123', timestamp: '12.12.1212.', stars: 4},
    // {username: 'test', filmId: 'f123', timestamp: '12.12.1212.', stars: 4},
    // {username: 'test', filmId: 'f123', timestamp: '12.12.1212.', stars: 4}
  ];

  constructor(private service: RatingService) {}

  ngOnInit(): void {
    this.service.get(this.filmId).subscribe({
      next: (data: Rating[]) => {
        this.ratings = data;
      },
      error: (_ => console.error('Error getting ratings'))
    });
  }


  rateStar(rating: number): void {
    this.noRating = false;
    for (let i=0; i<rating; i++) {
      this.stars[i] = true;
    }
    for (let i=rating; i<5; i++) {
      this.stars[i] = false;
    }
    this.rating = rating;
  }

  

  saveReview(): void {
    if (this.rating==0) {
      this.noRating = true;
      return;
    }

    //TODO
    const username = 'test';
    
    const dto: Rating = {
      filmId: this.filmId,
      username: username,
      stars: this.rating
    }

      this.service.rate(dto).subscribe({
        next: (response: MessageResponse) => {
          console.log(response.message);
        },
        error: (error: MessageResponse) => {
          console.log(error.message);
        }
      })
  }

}
