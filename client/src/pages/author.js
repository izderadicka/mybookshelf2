import {inject, bindable, computedFrom, LogManager} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
const logger = LogManager.getLogger('search');

@inject(ApiClient)
export class Author {
  _loader;
  @bindable filter;

  constructor(client) {
    this.client=client;
  }

  activate(params)  {
    logger.debug('Author activated with '+JSON.stringify(params));
    this.lastname=decodeURIComponent(params.lastname);
    this.firstname=params.firstname?decodeURIComponent(params.firstname):undefined
    this.updateLoader()
  }

  filterChanged() {
    logger.debug('Filter changed to '+ this.filter);
    this.updateLoader()
  }

  updateLoader() {
    this._loader = this.client.authorBooks.bind(this.client, this.lastname, this.firstname, this.filter);
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }

}
