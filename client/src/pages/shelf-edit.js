import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Ebook} from 'models/ebook';
import {DialogService} from 'aurelia-dialog';
import {Edit} from './abstract/edit';
import {Bookshelf} from 'models/bookshelf';

let logger = LogManager.getLogger('shelf-edit')

@inject(ApiClient, Router, Access, DialogService)
export class EditEbook extends Edit{

  constructor(client, router, access, dialog) {
    super(client, router, access, dialog);
    this.viewRoute = 'shelf';
    this.modelEntity = 'bookshelves';
    this.modelClass = Bookshelf;
    this.afterDeleteRoute = 'shelves';
  }


  get deleteConfirmMessage() {
    return `Do you want to delete bookshelf ${this.model.name}?`;
  }

}
