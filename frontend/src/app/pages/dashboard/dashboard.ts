import { Component, inject, OnInit } from '@angular/core';
import { Navbar } from '../../navbar/navbar';
import { FormsModule } from '@angular/forms';
import { Backendservice, EmailData } from '../../services/backendservice';
import { Router } from '@angular/router';
import { EventBusService } from '../../services/event-bus-service';
import { CommonModule } from '@angular/common'; // <-- Add this


@Component({
  selector: 'app-dashboard',
    standalone: true,  // <-- Make sure this is set if using imports
  imports: [Navbar, FormsModule, CommonModule], // <-- Add CommonModule here
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit{
  batches = null;
  loading = false;
  error = false;

  constructor(private backendservice: Backendservice, private router: Router){}

  private readonly eventBus = inject(EventBusService);

  ngOnInit() {
    // Retrieve the 'id' from the route
    let uid = sessionStorage.getItem('unique_id')!
    this.backendservice.getAllBatches(uid).subscribe({
      next: (res: any) => {
        this.batches = res
        console.log(res)
      },
      error: (err: any) => {
        console.error('Error retrieving batch', err);
      }
    });
  }

  emaildata: EmailData = {
    name: '',
    university: '',
    program: '',
    // prompt: '',
    file: null,
    unique_id: null,
  };

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.emaildata.file = file;
    }
  }

  emailSubmission() {
    this.loading = true;
    this.emaildata.unique_id = sessionStorage.getItem('unique_id');
    console.log("retrieved!!!" + this.emaildata.unique_id)
    console.log(this.emaildata)

    const formData = new FormData();
    formData.append('name', this.emaildata.name);
    formData.append('university', this.emaildata.university);
    formData.append('program', this.emaildata.program);
    // formData.append('prompt', this.emaildata.prompt || '');
    formData.append('unique_id', this.emaildata.unique_id || '');
    if (this.emaildata.file) {
      formData.append('file', this.emaildata.file);
    }

    this.backendservice.sendEmail(formData).subscribe({
      next: (res: any) => {
        this.loading = false;
        this.error = false;
        console.log(res['message'])
        console.log(res['id'])
        sessionStorage.setItem('currentbatchid', res['id'])
        this.router.navigate(['/dashboard/result', this.emaildata.unique_id, res['id']])
      },
      error: (err: any) => {
        console.error('Error generating draft', err);
        this.loading = false; // <- hide spinner if error
        this.error = true;
      }
    });
  }

  goToBatch(batchId: number) {
    this.router.navigate(['/dashboard/result', sessionStorage.getItem('unique_id'), batchId]);
  }

}

