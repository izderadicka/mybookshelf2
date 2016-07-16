import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';

@inject(ApiClient)
export class TestPage {
  country;
  series;
  seriesSelected;
  ebook;

  constructor(client) {
    this.client=client;
  }

  get seriesSelectedRepr() {
    return JSON.stringify(this.seriesSelected);
  }

  get loaderSeries() {
    return start => this.client.getIndex('series', start);
  }

  get loaderEbooks() {
    return start => this.client.getIndex('ebooks', start);
  }

  get loaderAuthors() {
    return start => this.client.getIndex('authors', start);
  }

  getFullName(item) {
    return item.first_name ? item.last_name + ', ' + item.first_name : item.last_name
  }
}
