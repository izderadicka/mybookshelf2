import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';

@inject(ApiClient)
export class TestPage {
  country;
  series;
  seriesSelected;

  constructor(client) {
    this.client=client;
  }

  get seriesSelectedRepr() {
    return JSON.stringify(this.seriesSelected);
  }

  get loaderSeries() {
    return start => this.client.getIndex('series', start);
  }
}
