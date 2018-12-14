import { HomeComponent } from './home/home.component';
import { CategoriasComponent } from './categorias/categorias.component';
import { JobsComponent } from './jobs/jobs.component';
import { UsuariosComponent } from './usuarios/usuarios.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MasterpageComponent } from './masterpage/masterpage.component';

const routes: Routes = [
  {
    path: '',
    component: MasterpageComponent,
    children: [
      {
        path: '',
        component: HomeComponent
      },
      {
        path: 'usuarios',
        component: UsuariosComponent
      },
      {
        path: 'jobs',
        component: JobsComponent
      },
      {
        path: 'categorias',
        component: CategoriasComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
