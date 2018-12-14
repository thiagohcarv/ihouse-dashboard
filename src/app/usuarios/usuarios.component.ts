import { Job } from './../interfaces/job';
import { AngularFireDatabase, AngularFireList } from '@angular/fire/database';
import { User } from './../interfaces/user';
import { DataBaseService } from './../services/data-base.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-usuarios',
  templateUrl: './usuarios.component.html',
  styleUrls: ['./usuarios.component.scss']
})
export class UsuariosComponent implements OnInit {
  users: User[] = [];
  usersBlocked: User[] = [];
  usersRef: AngularFireList<User>;
  userSelected: User;
  jobsUser: Job[] = [];

  constructor(private db: DataBaseService, private angularFireDB: AngularFireDatabase) { }

  ngOnInit() {
    this.usersRef = this.angularFireDB.list('user');
    this.usersRef.snapshotChanges().subscribe(d =>{
      d.forEach(u => {
        this.users.push({
          id : u['key'].toString() || '',
          address : u.payload.val()['address'],
          isAutorized : u.payload.val()['isAutorized'],
          name : u.payload.val()['name'],
          phone: u.payload.val()['phone'],
          rating: u.payload.val()['rating'],
          skills: u.payload.val()['skills'] || [],
          ssn: u.payload.val()['ssn'] || '',
          type: u.payload.val()['type'],
          urlPhoto: u.payload.val()['urlPhoto'],
          uuid: u.payload.val()['uuid']
        });
      });
      this.usersBlocked = this.users.filter((u) => { return u.isAutorized == false} );
      console.log(this.users);
    });

    // this.db.getEmployees<any>().subscribe((data: any[]) => {
    //   this.users = data;
    //   this.usersBlocked = this.users.filter((u) => { return u.isAutorized == false} );
    //   console.log(data);
    // }, (e) => console.log(e));
  }

  lock(u: User){
    u.isAutorized = false;
    this.db.updateUser(u.id, {
      address : u.address,
      isAutorized : u.isAutorized,
      name : u.name,
      phone: u.phone,
      rating: u.rating,
      skills: u.skills,
      ssn: u.ssn || '',
      type: u.type,
      urlPhoto: u.urlPhoto,
      uuid: u.uuid
    })
  }

  view(u: User){
    this.userSelected = u;
    this.getJobsUser(u);
  }

  getJobsUser(u: User){
    this.db.getJobsByEmployer(u.id).subscribe((d: Job[]) => {
      console.log(d);
      this.jobsUser = d;
    }, (e) => {
      console.log(e);
    })
  }

  unLock(u: User){
    u.isAutorized = true;
    this.db.updateUser(u.id, {
      address : u.address,
      isAutorized : u.isAutorized,
      name : u.name,
      phone: u.phone,
      rating: u.rating,
      skills: u.skills,
      ssn: u.ssn || '',
      type: u.type,
      urlPhoto: u.urlPhoto,
      uuid: u.uuid || null
    })
  }

  delete(u: User){
    if(confirm('Deseja mesmo remover este usuário?')){
      this.db.removeUserByID(u.id).then(() =>{
        alert('Usuário removido com sucesso');
      })
    }
    return;
  }


}
