import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Backendservice } from '../../services/backendservice';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';


@Component({
  selector: 'app-result',
  standalone: true,
  templateUrl: './result.html',
  styleUrl: './result.scss',
  imports: [CommonModule],
})
export class Result implements OnInit {

  id!: string;
  uid!: string;
  res: any;
  user_full_name!: string;

  constructor(private readonly route: ActivatedRoute, private readonly backendservice: Backendservice, private readonly router: Router) {}

  ngOnInit() {
    // Retrieve the 'id' from the route
    this.id = this.route.snapshot.paramMap.get('id')!;
    this.uid = this.route.snapshot.paramMap.get('uid')!;

    console.log('Retrieved ID:', this.id);
    console.log('Retrieved UID:', this.uid);

    this.backendservice.getBatch(this.id, this.uid).subscribe({
    next: (res: any) => {
      this.res = res

      this.user_full_name = res.user_full_name
      console.log(res)
    },
      error: (err: any) => {
        console.error('Error retrieving batch', err);
      }
    });
  }


  returnToDashboard(){
    this.router.navigate(['/dashboard'])
  }


  copyEmail(draft: any){
  // Ensure content is an object
  const content = typeof draft.content === 'string' ? JSON.parse(draft.content) : draft.content;

    const emailText = `${content.greeting}
    
    ${content.paragraph1}

    ${content.paragraph2}
    
    ${content.paragraph3}


    ${content.closing}
      
    ${this.user_full_name || ''}  
    `;

    navigator.clipboard.writeText(emailText).then(() => {
      alert('Email copied to clipboard!');
    });
  }
}
