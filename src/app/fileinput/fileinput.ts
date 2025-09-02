import { Component, OnInit } from '@angular/core';
import { Geminiservice } from './geminiservice';

@Component({
  selector: 'app-fileinput',
  imports: [],
  templateUrl: './fileinput.html',
  styleUrl: './fileinput.css',
  standalone: true,
})
export class Fileinput implements OnInit {

  constructor(private geminiservice: Geminiservice){

  }

  ngOnInit(){
  }
}
