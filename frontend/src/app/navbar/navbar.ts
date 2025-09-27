import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss'
})
export class Navbar implements OnInit{

  ngOnInit(): void {
      
  }

  constructor(private readonly router: Router){}
  navigateHome(){
    this.router.navigate(['/'], { relativeTo: this.router.routerState.root });
  }
}
