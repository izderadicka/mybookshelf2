import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';

const logger = LogManager.getLogger('shelves');

@inject(ApiClient)
export class Shelves {
  sortings = [{name:'Name A-Z', key:'name'}, {name:'Name Z-A', key:'-name'},
              {name:'Recent First', key: 'created'}, {name:'Oldest First', key: '-created'}]
  constructor(client) {
    this.client = client;
  }

  activate() {
    this.updateLoader();
  }

  updateLoader() {
    this._loader = (page, pageSize, sort) =>
      this.client.getMany('bookshelves', page, pageSize, sort, {filter:this.filter});
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }
  }
