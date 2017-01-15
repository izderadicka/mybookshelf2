import {inject, LogManager, computedFrom, bindable} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';

const logger = LogManager.getLogger('ebook-conversions');

@inject(ApiClient, Access)
export class EbookConversions {
  sortings = [{name:'Recent First', key:'-created'}, {name:'Oldest First', key:'created'} ];
  constructor(client, access) {
    this.client = client;
    this.access = access;
    this.token = access.token;
  }

  activate() {
    this.updateLoader();
  }

  updateLoader() {
    this._loader = (page, pageSize, sort) =>
      this.client.getMany('conversions/mime', page, pageSize, sort);
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }

  deleteItem(item) {
  }
}
