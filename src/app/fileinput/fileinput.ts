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

  instructions = {
    inputInstructions: "",
    formatInstructions: "",
  }

  constructor(private geminiservice: Geminiservice){

  }

  ngOnInit(){
  }

  sendFile(event: HTMLInputElement){

    let file = event.files!
    let filedata = this.geminiservice.parseFile(file[0])
    console.log(filedata);
    
  //  let file_element = document.getElementById("file")!;
  //   console.log(file_element.file)
  //   console.log(this.geminiservice.generateResponse("test this"))
  }
}
