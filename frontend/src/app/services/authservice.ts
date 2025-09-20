import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Authservice {
  constructor(private http: HttpClient) {}

  signup(data: any) {
    return this.http.post('/api/signup', data);
  }

  login(data: any) {
    return this.http.post('/api/login', data);
  }
}
