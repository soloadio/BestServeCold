import { TestBed } from '@angular/core/testing';

import { Geminiservice } from './geminiservice';

describe('Geminiservice', () => {
  let service: Geminiservice;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Geminiservice);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
