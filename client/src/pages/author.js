import {inject, computedFrom, LogManager} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
const logger = LogManager.getLogger('search');

@inject(ApiClient)
export class Author {
  _loader
  constructor(client) {
    this.client=client;
  }

  activate(params)  {
    logger.debug('Author activated with '+JSON.stringify(params));
    this.lastname=decodeURIComponent(params.lastname);
    this.firstname=params.firstname?decodeURIComponent(params.firstname):undefined
    this._loader = this.client.authorBooks.bind(this.client, this.lastname, this.firstname);
  }



  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }
}
