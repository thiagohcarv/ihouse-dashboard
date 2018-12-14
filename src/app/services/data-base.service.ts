import { Injectable } from '@angular/core';
import { AngularFireDatabase } from '@angular/fire/database';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataBaseService {

  constructor(private db: AngularFireDatabase) { }

  getCategories<T>(): Observable<T[]> {
    return this.db.list<T>("category").valueChanges();
  }
  getMessages<T>(): Observable<T[]> {
    return this.db.list<T>("messages").valueChanges();
  }
  createUser<T>(path: string, user: T): void {
    this.db.object<T>(path).set(user);
  }
  createCategory<T>(cat: T): void {
    console.log(cat);
    this.db.object<T>(`category/${cat['id']}`).set(cat);
  }
  updateUser<T>(id: string, params: any): Promise<void> {
    const ref = this.db.object<T>(`user/${id}`);
    return ref.update(params);
  }

  // Job

  createJob<T>(path: string, job: T): void {
    this.db.object<T>(path).set(job);
  }

  getJobsByEmployer<T>(id: string): Observable<T[]> {
    return this.db.list<T>(`jobs/${id}`).valueChanges();
  }

  getJobs<T>(): Observable<T[]> {
    return this.db.list<T>("jobs").valueChanges();
  }

  getJobsByCategory<T>(categoryID: number): Observable<T[]> {
    return this.db.list<T>("/jobs", (ref) =>
      ref.orderByChild('category').equalTo(categoryID)
    ).valueChanges();
  }

  // Employee

  getUserByID<T>(id: string): Observable<T> {
    return this.db.object<T>(`user/${id}`).valueChanges();
  }

  getEmployees<T>(): Observable<T[]> {
    return this.db.list<T>("user").valueChanges();
  }

  getEmployeeByID<T>(id: string): Observable<T> {
    return this.db.object<T>(`user/${id}`).valueChanges();
  }

  // Employer

  getEmployers<T>(): Observable<T[]> {
    return this.db.list<T>("user").valueChanges();
  }

  getEmployerByID<T>(id: string): Observable<T> {
    return this.db.object<T>(`user/${id}`).valueChanges();
  }

  removeUserByID<T>(id: string): Promise<void> {
    const ref = this.db.object<T>(`user/${id}`);
    return ref.remove();
  }

}
