import {inject, bindable} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {rewriteURLParam} from 'lib/utils';

const logger = LogManager.getLogger('welcome');

@inject(ApiClient)
export class Welcome {

  constructor(client) {
    this.client = client;
  }

  activate() {
    this.loadEbooks(48);
  }

  loadEbooks(size) {
    this.client.getMany('ebooks', 1, size, '-created')
    .then(res => this.ebooks=res.data)
    .catch(err => logger.error('Fetch error', err));
  }


}
