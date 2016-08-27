
import {inject, bindable, LogManager} from 'aurelia-framework';
import {HttpClient} from 'aurelia-fetch-client';

const logger=LogManager.getLogger('ebooks-panel');

@inject(HttpClient)
export class EbookPanel {
  @bindable sortings=[{name:'Title A-Z', key:'title'}, {name:'Title Z-A',key:'-title'},
      {name:'Recent First', key:'-created'}, {name:'Oldest First', key: 'created'}];
  @bindable loader;

  constructor(http) {
    this.http=http;
  }

  loaderChanged() {
    logger.debug('Loader changed in EbookPanel');
  }

  getThumbSource(ebook) {
    return this.http.baseUrl +'/thumb/'+ebook.id;
  }
}
