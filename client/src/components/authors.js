
import {bindable, computedFrom} from 'aurelia-framework';
export class Authors {
  @bindable authors=[];
  @bindable compact=false;
  @bindable linked = true;

  @computedFrom('authors', 'compact')
  get many() {
    if (!this.authors) return false;
    return this.authors.length > 2 && this.compact;
  }
}
