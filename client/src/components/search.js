import {bindable, inject} from 'aurelia-framework';
import $ from 'jquery';

@inject(Element)
export class Search {
  @bindable query;
  @bindable execute;

  constructor(elem) {
    this.elem=elem;
  }

  executeSearch() {

    if (this.query) this.execute({query:this.query});
  }

  clearSearch(evt) {
    let search = $('input', this.elem);
    this.query = '';
    search.focus();
  }
}
