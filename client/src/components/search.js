import {bindable} from 'aurelia-framework';

export class Search {
  @bindable query;
  @bindable execute;

  executeSearch() {

    if (this.query) this.execute({query:this.query});
  }
}
