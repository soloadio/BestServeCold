import { Component } from '@angular/core';
import { Navbar } from '../../navbar/navbar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [Navbar],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home {

  constructor(private router: Router) {}

  signup(){
    console.log("Signup clicked");
    this.router.navigate(['signup'], { relativeTo: this.router.routerState.root });
  }

  login(){
    console.log("Login clicked");
    this.router.navigate(['login'], { relativeTo: this.router.routerState.root });
  }
}
