import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {Access} from 'lib/access';

let logger = LogManager.getLogger('ebooks');

@inject(ApiClient, Access)
export class Ebook {
  ebook
  constructor(client, access, ) {
    this.client=client;
    this.access=access;
    this.token=access.token;
    this.canDownload=access.hasRole('user');
    this.canConvert=access.hasRole('user');
  }

  activate(params) {
    this.client.getOne('ebooks', params.id)
      .then(b => this.ebook=b)
      .catch(err => logger.error(`Failed to load ${err}`));
  }

}
