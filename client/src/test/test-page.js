import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';

@inject(ApiClient)
export class TestPage {
  constructor(client) {
    this.client=client;
  }

  get loaderSeries() {
    return start => this.client.getIndex('series', start);
  }
}
