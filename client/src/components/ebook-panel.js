
import {inject, bindable, LogManager} from 'aurelia-framework';
import {HttpClient} from 'aurelia-fetch-client';
import $ from 'jquery';

const logger=LogManager.getLogger('eboos-panel');

export class EbookPanel {
  @bindable sortings=[{name:'Title A-Z', key:'title'}, {name:'Title Z-A',key:'-title'},
      {name:'Recent First', key:'-created'}, {name:'Oldest First', key: 'created'},
      {name: 'Best Rated', key:'-rating'}, {name: 'Worst Rated', key: 'rating'}];
  @bindable loader;


  loaderChanged() {
    logger.debug('Loader changed in EbookPanel');
  }

}
