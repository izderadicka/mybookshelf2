import {inject, LogManager, computedFrom, bindable} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';

const logger = LogManager.getLogger('shelves');

@inject(ApiClient)
export class Shelves {
  sortings = [{name:'Name A-Z', key:'name'}, {name:'Name Z-A', key:'-name'},
              {name:'Recent First', key: 'created'}, {name:'Oldest First', key: '-created'}]

  @bindable filter;
  constructor(client) {
    this.client = client;
    this.mine = true;
  }

  activate() {
    this.updateLoader();
  }

  updateLoader() {
    this._loader = (page, pageSize, sort) =>
      this.client.getMany(`bookshelves/${this.mine?'mine':'others'}`, page, pageSize, sort, {filter:this.filter});
  }


  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }

  changeTab() {
    this.mine = ! this.mine;
    let oldFilter = this.filter;
    this.filter = null;
    if (oldFilter === null) this.updateLoader();
  }

  filterChanged() {
    this.updateLoader();
  }
}
