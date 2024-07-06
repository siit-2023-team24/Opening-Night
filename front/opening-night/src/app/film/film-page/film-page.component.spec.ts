import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilmPageComponent } from './film-page.component';

describe('FilmPageComponent', () => {
  let component: FilmPageComponent;
  let fixture: ComponentFixture<FilmPageComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FilmPageComponent]
    });
    fixture = TestBed.createComponent(FilmPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
