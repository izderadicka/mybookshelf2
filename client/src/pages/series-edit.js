import {inject} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Series} from 'models/series';
import {DialogService} from 'aurelia-dialog';
import {Edit} from './abstract/edit';

@inject(ApiClient, Router, Access, DialogService)
export class EditSeries extends Edit{

  constructor(client, router, access, dialog) {
    super(client, router, access, dialog);
    this.viewRoute = 'series';
    this.modelEntity = 'series';
    this.modelClass = Series;
    //this.afterDeleteRoute = 'shelves';
  }

  canDelete() {
    return false;
  }

  canEdit() {
    return this.model.id && this.access.hasRole('superuser');
  }

  doAfterSave() {
    this.client.clearCache('ebooks');
    return Promise.resolve();
  }
}
