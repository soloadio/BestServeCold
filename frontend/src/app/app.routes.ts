import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Signup } from './pages/signup/signup';

export const routes: Routes = [

    {component: Home, path: ''},
    {component: Signup, path: 'signup'},

];
