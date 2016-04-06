import {inject, computedFrom, LogManager} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
const logger = LogManager.getLogger('search');

@inject(ApiClient)
export class Search {
  _loader
  constructor(client) {
    this.client=client;
  }

  activate(params)  {
    logger.debug('Search actited with '+JSON.stringify(params));
    this.query=decodeURIComponent(params.query);
    this._loader = this.client.search.bind(this.client, this.query);
  }

  bind(ctx, newCtx) {
    logger.debug('Search bind');
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }
}
