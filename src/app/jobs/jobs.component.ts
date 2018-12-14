import { Job } from './../interfaces/job';
import { DataBaseService } from './../services/data-base.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit {

  jobs: Job[] = [];

  constructor(private db: DataBaseService) { }

  ngOnInit() {
    this.db.getJobs<Job>().subscribe((data: Job[]) => {
      this.jobs = data;
      this.jobs.forEach(j =>{
        let date = new Date(j.timestamp);
        j.timestamp = date.getMonth() +"/"+date.getDate()+"/"+date.getFullYear();
      })
      console.log(this.jobs);
    }, (e) => console.log(e));
  }

}
