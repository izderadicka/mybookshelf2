import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';

@inject(Router, ApiClient)
export class AddToShelfButton {
  @bindable what
  @bindable item
  constructor(router, client) {
    this.client = client;
    this.router = router;
  }

  showAddToShelf() {
    this.router.navigateToRoute('add-to-shelf', {what:this.what, id:this.item.id})
  }
}
