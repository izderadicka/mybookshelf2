import {inject} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Author} from 'models/author';
import {DialogService} from 'aurelia-dialog';
import {Edit} from './abstract/edit';

@inject(ApiClient, Router, Access, DialogService)
export class EditEbook extends Edit{

  constructor(client, router, access, dialog) {
    super(client, router, access, dialog);
    this.viewRoute = 'author';
    this.modelEntity = 'authors';
    this.modelClass = Author;
    //this.afterDeleteRoute = 'shelves';
  }

  canDelete() {
    return false;
  }

  canEdit() {
    return this.model.id && this.access.hasRole('superuser');
  }


/*
  get deleteConfirmMessage() {
    return `Do you want to delete bookshelf ${this.model.name}?`;
  }
  */

}
