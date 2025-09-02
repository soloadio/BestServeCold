import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Fileinput } from './fileinput';

describe('Fileinput', () => {
  let component: Fileinput;
  let fixture: ComponentFixture<Fileinput>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Fileinput]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Fileinput);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
