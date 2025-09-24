import { Component, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnInit{
  protected readonly title = signal('frontend');

  ngOnInit(): void {
    // @ts-ignore
    window.handleCredentialResponse = (response) => {
      console.log("Encoded JWT ID token: " + response.credential);
    };
    // const script = document.createElement('script');
    // script.src = 'https://accounts.google.com/gsi/client';
    // script.async = true;
    // script.defer = true;
    // document.body.appendChild(script);
  }
}
