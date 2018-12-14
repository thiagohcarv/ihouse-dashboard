import { SanitizeHtmlPipePipe } from './pipes/sanitize-html-pipe.pipe';
import { AngularFireDatabase } from '@angular/fire/database';
import { FirebaseConfig } from './../environments/firebase.config';
import { environment } from './../environments/environment';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MasterpageComponent } from './masterpage/masterpage.component';
import { UsuariosComponent } from './usuarios/usuarios.component';
import { JobsComponent } from './jobs/jobs.component';
import { CategoriasComponent } from './categorias/categorias.component';
import { AngularFireModule } from '@angular/fire';
import { AngularFirestore } from '@angular/fire/firestore';
import { HomeComponent } from './home/home.component';
import { FormsModule } from '@angular/forms'


@NgModule({
  declarations: [
    AppComponent,
    MasterpageComponent,
    UsuariosComponent,
    JobsComponent,
    CategoriasComponent,
    HomeComponent,
    SanitizeHtmlPipePipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    AngularFireModule.initializeApp(FirebaseConfig)
  ],
  providers: [AngularFireDatabase, AngularFirestore],
  bootstrap: [AppComponent]
})
export class AppModule { }
