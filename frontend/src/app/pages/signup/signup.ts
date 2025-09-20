import { Component } from '@angular/core';
import { Navbar } from '../../navbar/navbar';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-signup',
  imports: [Navbar, FormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.scss'
})
export class Signup {

  user = {
    name: '',
    email: '',
    password: '',
  }

  signup(){
    console.log("Signup clicked");
  }


  onSubmit(){
    console.log("Form submitted");
    console.log(this.user);
  }
}
