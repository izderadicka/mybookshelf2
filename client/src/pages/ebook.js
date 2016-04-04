import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
let logger = LogManager.getLogger('ebooks');

@inject(ApiClient)
export class Ebook {
  ebook
  constructor(client) {
    this.client=client;
  }

  activate(params) {
    this.client.getOne('ebooks', params.id)
      .then(b => this.ebook=b)
      .catch(err => logger.error(`Failed to load ${err}`));
  }

}
