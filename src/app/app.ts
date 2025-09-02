import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Fileinput } from './fileinput/fileinput';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Fileinput],
  templateUrl: './app.html',
  styleUrl: './app.css',
  standalone: true,
})
export class App {
  protected readonly title = signal('BestServeCold');
}
