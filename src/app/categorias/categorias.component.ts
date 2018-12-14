import { Category } from './../interfaces/category';
import { DataBaseService } from './../services/data-base.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-categorias',
  templateUrl: './categorias.component.html',
  styleUrls: ['./categorias.component.scss']
})
export class CategoriasComponent implements OnInit {
  categories: Category[] = [];
  newCategory: Category = null;
  base64textString: string;
  name: string;
  value: number;

  constructor(private db: DataBaseService) { }

  ngOnInit() {
    this.db.getCategories<Category>().subscribe((res) => {
      this.categories = res;
      console.log(this.categories);
    }, (err) => {
      console.log(err);
    })
  }

  save(){
    let id = 1
    if (this.categories.length) {
      id = this.categories[this.categories.length -1].id +1 || 1
    }
    this.db.createCategory<Category>({
      id : id,
      img : this.base64textString || null,
      name: this.name,
      value: this.value || null
    });
  }


  onChangeFile(event){
    let files = event.target.files
    let file = files[0];
    if(files && file){
      const reader = new FileReader();
      reader.onload = this._handleReaderLoaded.bind(this);
      reader.readAsBinaryString(file);
    }
  }

  _handleReaderLoaded(readerEvt) {
    var binaryString = readerEvt.target.result;
    this.base64textString = 'data:image/png;base64,' + btoa(binaryString);
   }

}
