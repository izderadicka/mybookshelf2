import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access'

const logger = LogManager.getLogger('shelf');

@inject(ApiClient, Access)
export class Shelf {
  sortings = [{name:'Order A-Z', key:'order'}, {name:'Order Z-A', key:'-order'},
              {name:'Recent First', key:'-created'}, {name:'Oldest First', key:'created'} ]
  constructor(client, access) {
    this.client = client;
    this.access = access;
    this._loader = null;

  }

  setError(error, errorDetail) {
    self.error = {error, errorDetail};
    logger.error(error, errorDetail);
  }

  canActivate(params) {
    return this.client.getOne('bookshelves', params.id)
    .then(data => {
      this.shelf = data;
      return true;
      })
    .catch(error => {
      this.setError('Cannot load shelf', error);
      return false;
    });
  }

  activate() {
    this.updateLoader();
  }

  updateLoader() {
    this._loader = (page, pageSize, sort) =>
      this.client.getMany(`bookshelves/${this.shelf.id}/items`, page, pageSize, sort);
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }

  get isEditable() {
    return this.shelf && this.access.canEdit(this.shelf.created_by);
  }

  get editActions() {
    return [{text:"Information",value:'edit', icon:'info-circle'},
      {text:'Merge', value:'merge', icon:'compress'}];
  }

  get editAction() {
    return action => {
    switch (action) {
      case 'edit':
        this.router.navigateToRoute('shelf-edit', {id:this.shelf.id})
      break;
      case 'merge':
      this.router.navigateToRoute('shelf-merge', {id: this.shelf.id});
      break;
    }
  }
  }


}
