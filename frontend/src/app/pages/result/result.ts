import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Backendservice } from '../../services/backendservice';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Navbar } from '../../navbar/navbar';


@Component({
  selector: 'app-result',
  standalone: true,
  templateUrl: './result.html',
  styleUrl: './result.scss',
  imports: [CommonModule, Navbar],
})
export class Result implements OnInit {

  loading = true;
  error = false;

  sent = false;
  senderror = false

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
      this.loading = false;
      this.error = false;
      this.res = res

      this.user_full_name = res.user_full_name
      console.log(res)
    },
      error: (err: any) => {
        console.error('Error retrieving batch', err);
        this.loading = false
        this.error = true
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

${this.user_full_name || ''}`;

    navigator.clipboard.writeText(emailText).then(() => {
      alert('Email copied to clipboard!');
    });
  }

async draftEmail(draft: any) {

  let toEmail = draft.email
  let subject = draft.content.subject
  let accessToken = sessionStorage.getItem('access_token')
  console.log(`this is my accesstoken ${accessToken}`)
  // Parse content if needed
  const content = typeof draft.content === 'string' ? JSON.parse(draft.content) : draft.content;

  // Build email text
const emailText = `${content.greeting}

${content.paragraph1}

${content.paragraph2}

${content.paragraph3}


${content.closing}

${this.user_full_name || ''}`;

  // Construct raw MIME message
  const message =
    `To: ${toEmail}\r\n` +
    `Subject: ${subject}\r\n` +
    `Content-Type: text/plain; charset="UTF-8"\r\n\r\n` +
    `${emailText}`;

  // Convert to Base64URL
  const encodedMessage = btoa(message)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  try {
    const response = await fetch('https://gmail.googleapis.com/gmail/v1/users/me/drafts', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: { raw: encodedMessage }
      })
    });

    if (!response.ok) throw new Error(`Error: ${response.statusText}`);

    const data = await response.json();
    console.log('Draft created:', data);
    this.senderror = false;
    this.sent = true;
  } catch (error) {
    console.error('Failed to create draft:', error);
    this.sent = false;
    this.senderror = true;
  }
}
  async draftAllEmail() {
    for (let draft of this.res.drafts as any[]) {
      this.draftEmail(draft);
    }
  }

}
