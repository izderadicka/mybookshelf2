import {inject, LogManager, bindable, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';

const logger = LogManager.getLogger('series');

@inject(ApiClient)
export class Series {
  sortings=[{name:'Series Index Asc.', key:'series_index'},
            {name:'Series Index Desc.', key:'-series_index'},
            {name:'Title A-Z', key:'title'},
            {name:'Title Z-A',key:'-title'},
            {name:'Recent First', key:'-created'},
            {name:'Oldest First', key: 'created'}];
  constructor(client) {
    this.client=client;
  }

  canActivate(params) {
    this.loader = this.client.getMany.bind(this.client,'ebooks/series/'+params.id);
    this.client.getOne('series', params.id)
    .then( s => {
      this.series = s;
      return true;
    })
    .catch(err => {
      logger.error(`Fetch error ${err}`, err);
      return false;
    });
  }
}
