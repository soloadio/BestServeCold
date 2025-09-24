import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Dashboard } from './pages/dashboard/dashboard';
import { Result } from './pages/result/result';

export const routes: Routes = [

    {component: Home, path: ''},
    {component: Dashboard, path: 'dashboard'},
    {component: Result, path: 'dashboard/result/:uid/:id'}

];
