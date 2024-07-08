import { Component, OnInit } from '@angular/core';
import { FilmFeedDTO } from '../model/film_feed';
import { FilmService } from '../film.service';
import { MessageResponse } from 'src/env/error-response';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  styleUrls: ['./feed.component.css']
})
export class FeedComponent implements OnInit {

  films: FilmFeedDTO[] = []

  constructor(private service: FilmService) {}

  ngOnInit(): void {
    //TODO
    const username = 'test';

    this.service.getFeed(username).subscribe({
      next: (data: FilmFeedDTO[]) => {
        this.films = data;
        console.log(data)
      },
      error: (error: MessageResponse) => console.log(error.message)
    })

    // this.films = [{
    //   actors: ['Brie Larsen', 'Samuel L. Jackson'],
    //   directors: ['ne znam'],
    //   fileName: "captainmarvelmp4",
    //   genres: ['drama', 'comedy', 'superhero'],
    //   title: "Captain Marvel (2019)",
    //   isSeries: false
    // }]
  }

}
