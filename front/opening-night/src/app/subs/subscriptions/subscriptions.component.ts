import { Component, OnInit } from '@angular/core';
import { SubsService } from '../subs.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SubscriptionDTO } from '../model/subscription';
import { Genre } from 'src/app/shared/genre';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MessageResponse } from 'src/env/error-response';
import { ActorsAndDirectorsDTO } from 'src/app/shared/actorsAndDirectors';


@Component({
  selector: 'app-subscriptions',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.css']
})
export class SubscriptionsComponent implements OnInit {

  subscription: SubscriptionDTO = {directors: [], actors: [], genres: []}

  username = "";
  email = "parabucki.sonja@gmail.com"

  genres = Object.values(Genre)
  directors: string[] = []
  actors: string[] = []

  genreForm: FormGroup;
  directorsForm: FormGroup;
  actorsForm: FormGroup;

  newDirector = "";
  newActor = "";

  constructor(private service: SubsService,
              private formBuilder: FormBuilder,
              private snackBar: MatSnackBar) {
    this.genreForm = this.formBuilder.group({genre: [null]})
    this.directorsForm = this.formBuilder.group({director: [null]});
    this.actorsForm = this.formBuilder.group({actor: [null]});
  }

  ngOnInit(): void {

    //TODO get username
    this.username = "test"

    this.service.get(this.username).subscribe({
      next: (data: SubscriptionDTO) => {
        this.subscription = data
      },
      error: () => console.error('Error getting subscriptions')
    });

    this.service.getActorsAndDirectors().subscribe({
      next: (data: ActorsAndDirectorsDTO) => {
        this.directors = data.directors;
        this.directors.sort()
        this.actors = data.actors
        this.actors.sort()
      }
    })

    this.genres = this.genres.filter(g => this.subscription.genres.indexOf(g) == -1);

  }


  subscribeToGenre(): void {
    const g = this.genreForm.get('genre')?.value;
    if (!g) {
      this.showSnackBar("No genre is selected.");
      return;
    }
    console.log('Selected genre:', g);
    this.addToList(this.subscription.genres, g);
    this.removeFromList(this.genres, g);
    // this.updateSubs();
  }

  subscribeToDirector(): void {
    const d = this.directorsForm.get('director')?.value;
    if (!d) {
      this.showSnackBar("No director is selected.");
      return;
    }
    console.log('Selected director: ', d);
    this.addToList(this.subscription.directors, d)
    this.removeFromList(this.directors, d);
    // this.updateSubs();
  }

  subscribeToNewDirector(): void {
    if (!this.newDirector) {
      this.showSnackBar("Director is not specified.");
      return;
    }
    console.log('Selected director: ', this.newDirector);
    this.addToList(this.subscription.directors, this.newDirector);
    // this.updateSubs();
  }

  subscribeToActor(): void {
    const a = this.actorsForm.get('actor')?.value;
    if (!a) {
      this.showSnackBar("No actor is selected.");
      return;
    }
    console.log('Selected actor: ', a);
    this.addToList(this.subscription.actors, a)
    this.removeFromList(this.actors, a);
    // this.updateSubs();
  }

  subscribeToNewActor(): void {
    if (!this.newActor) {
      this.showSnackBar("Actor is not specified.");
      return;
    }
    console.log('Selected actor: ', this.newActor);
    this.addToList(this.subscription.actors, this.newActor)
    // this.updateSubs();
  }


  removeGenre(g: string): void {
    this.removeFromList(this.subscription.genres, g);
    this.addToList(this.genres, Genre[g as keyof typeof Genre]);
    // this.updateSubs();
  }

  removeDirector(d: string): void {
    this.removeFromList(this.subscription.directors, d);
    this.addToList(this.directors, d);
    // this.updateSubs();
  }

  removeActor(a: string): void {
    this.removeFromList(this.subscription.actors, a);
    this.addToList(this.actors, a);
    // this.updateSubs();
  }


  updateSubs(): void {
    if (!this.username) return;
    this.subscription.email = this.email
    console.log(this.subscription);

    this.service.update(this.username, this.subscription).subscribe({
      next: ((message: MessageResponse) => this.showSnackBar(message.message)),
      error: (_ => this.showSnackBar("An error occured."))
      });
  }

  private showSnackBar(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
    });
  }

  private addToList(list: Object[], obj: Object) {
    list.push(obj);
    list.sort();
  }

  private removeFromList(list: Object[], obj: Object) {
    list.splice(list.indexOf(obj), 1);
  }

}
