import { AfterViewInit, Component} from '@angular/core';
import { Navbar } from '../../navbar/navbar';
import { Router } from '@angular/router';
import { Backendservice } from '../../services/backendservice';
import { environment } from '../../../environments/environment';

declare const google: any;

@Component({
  selector: 'app-home',
  imports: [Navbar],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home implements AfterViewInit{

  ngAfterViewInit(): void {
    // Bind your credential handler to the global window object
    window.handleCredentialResponse = this.handleCredentialResponse.bind(this);

    // Check if the script already exists to avoid duplicate loading
    if (!document.getElementById('google-signin')) {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.id = 'google-signin';

      document.body.appendChild(script);
    }
  }

  constructor(private readonly router: Router, private readonly backendservice: Backendservice) {}

  login(){
    console.log("Login clicked");
    this.router.navigate(['login'], { relativeTo: this.router.routerState.root });
  }

  decodeJWT(token:any) {

    let base64Url = token.split(".")[1];
    let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    let jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map(function (c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join("")
    );
    return JSON.parse(jsonPayload);
  }

  handleCredentialResponse(response:any) {

    console.log("Encoded JWT ID token: " + response.credential);

    const responsePayload = this.decodeJWT(response.credential);

    console.log("why wony you print")
    const user = {
      full_name: responsePayload.name,
      given_name: responsePayload.given_name,
      unique_id: responsePayload.sub,
      email: responsePayload.email,
    };
    console.log("why wony you print2")
    console.log("Decoded User Object:", user);


    console.log("stored!!!")
    sessionStorage.setItem('unique_id', responsePayload.sub);
    console.log(sessionStorage.getItem('unique_id'))


    // --- Initialize OAuth token client for Gmail ---
    const tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: `${environment.CLIENT_ID}`,
      scope: 'https://www.googleapis.com/auth/gmail.compose',
      callback: (tokenResponse: any) => {
        console.log('Gmail access token:', tokenResponse.access_token);

        sessionStorage.setItem('access_token', tokenResponse.access_token);
        // You can now call Gmail API with this access token
      },
    });

    // Optional: request Gmail access immediately
    tokenClient.requestAccessToken();

    


    this.backendservice.login(user).subscribe({
      next: (res: any) => {
        console.log('User created or already exists:', res);
        this.router.navigate(['/dashboard'], { relativeTo: this.router.routerState.root });
      },
      error: (err: any) => {
        console.error('Error saving user:', err);
      }
    });
  }
}
