import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Router} from 'aurelia-router';
import {DialogService} from 'aurelia-dialog';
import {ShelfItemEditDialog} from './shelf-item-edit-dialog';
import {ConfirmDialog} from 'components/confirm-dialog';
import {ConvertMany} from './abstract/convert-many';
import {WSClient} from 'lib/ws-client';
import {Configure} from 'lib/config/index';


const logger = LogManager.getLogger('shelf');

@inject(ApiClient, Access, Router, DialogService, Configure, WSClient)
export class Shelf extends ConvertMany{
  sortings = [{name:'Order A-Z', key:'order'}, {name:'Order Z-A', key:'-order'},
              {name:'Recent First', key:'-created'}, {name:'Oldest First', key:'created'} ]
  constructor(client, access, router, dialog, config, wsClient) {
    super(access, config, wsClient);
    this.client = client;
    this.access = access;
    this.router = router;
    this._loader = null;
    this.dialog = dialog;
    this.entity = 'bookshelf';

  }

  setError(error, errorDetail) {
    self.error = {error, errorDetail};
    logger.error(error, errorDetail);
  }

  canActivate(params) {
    return this.client.getOne('bookshelves', params.id)
    .then(data => {
      this.bookshelf = data;
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
      this.client.getMany(`bookshelves/${this.bookshelf.id}/items`, page, pageSize, sort);
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }

  get isEditable() {
    return this.bookshelf && this.access.canEdit(this.bookshelf.created_by);
  }

  get editActions() {
    return [{text:"Information",value:'edit', icon:'info-circle'},
      {text:'Merge', value:'merge', icon:'compress'}];
  }

  get editAction() {
    return action => {
    switch (action) {
      case 'edit':
        this.router.navigateToRoute('shelf-edit', {id:this.bookshelf.id})
      break;
      case 'merge':
      this.router.navigateToRoute('shelf-merge', {id: this.bookshelf.id});
      break;
    }
  }
  }

  editItem(item) {
    return (evt) => {

      return this.dialog.open({viewModel: ShelfItemEditDialog, model:item})
      .then( result => {
        if (result.wasCancelled) {
          return 'noreload';
        } else {
          console.log(result);
        }
      });

    }
  }

  deleteItem(item) {
    return (evt) => {
      logger.debug('Deleting item '+item.id);
      return this.client.delete('bookshelf-items', item.id)
      .then(res => {
        if (res.error) {
          logger.error('Delete error', res.error);
        }
      })
      .catch( err => {
          logger.error('Delete error', err);
      })
    }
  }


}
