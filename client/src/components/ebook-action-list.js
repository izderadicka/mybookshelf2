import {bindable} from 'aurelia-framework';

export class EbookActionList {
  @bindable actionName = "Action"
  @bindable action
  @bindable ebooks

  get isMore() {
    return this.ebooks && this.ebooks.lastPage > 1;
  }


}
