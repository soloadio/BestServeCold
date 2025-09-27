// email.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';

export interface EmailData {
  name: string;
  university: string;
  program: string;
  file?: File | null;
  // prompt: string;
  unique_id: any
}

@Injectable({
  providedIn: 'root'
})
export class Backendservice {

  constructor(private readonly http: HttpClient, private readonly router: Router) {}

  sendEmail(data: FormData): Observable<any> {
    return this.http.post(`${environment.BACKEND_SERVER}/draftgenerator/`, data);
  }

  getBatch(batchId: string, uid: string) {
    return this.http.get(`${environment.BACKEND_SERVER}/batches?id=${batchId}&uid=${uid}`);
  }

  getAllBatches(uid: string){
    return this.http.get(`${environment.BACKEND_SERVER}/batches?uid=${uid}`);
  }

  login(user:any){
    return this.http.post(`${environment.BACKEND_SERVER}/users/`, user);
  }
}
