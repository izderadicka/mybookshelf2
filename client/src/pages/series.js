import {inject, LogManager, bindable, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Router} from 'aurelia-router';
import {Configure} from 'lib/config/index';
import {ConvertMany} from './abstract/convert-many';
import {WSClient} from 'lib/ws-client';

const logger = LogManager.getLogger('series');

@inject(ApiClient, Access, Router, Configure, WSClient)
export class Series extends ConvertMany{
  sortings=[{name:'Series Index Asc.', key:'series_index'},
            {name:'Series Index Desc.', key:'-series_index'},
            {name:'Title A-Z', key:'title'},
            {name:'Title Z-A',key:'-title'},
            {name:'Recent First', key:'-created'},
            {name:'Oldest First', key: 'created'}];
  constructor(client, access, router, config, wsClient) {
    super(access, config, wsClient);
    this.client=client;
    this.access=access;
    this.router=router;
    this.entity='series';
  }

  canActivate(params) {
    this.loader = this.client.getMany.bind(this.client,'ebooks/series/'+params.id);
    return this.client.getOne('series', params.id)
    .then( s => {
      this.series = s;
      return true;
    })
    .catch(err => {
      logger.error(`Fetch error ${err}`, err);
      return false;
    });
  }

  activate(params, route) {
    route.navModel.setTitle(`Series "${this.series.title}"`);
  }

  get editActions() {
    return [{text:"Information",value:'edit', icon:'info-circle'},
      {text:'Merge', value:'merge', icon:'compress'}];

  }

  get editAction() {
    return action => {
    switch (action) {
      case 'edit':
        this.router.navigateToRoute('series-edit', {id:this.series.id})
      break;
      case 'merge':
      this.router.navigateToRoute('series-merge', {id: this.series.id});
      break;
    }
  }
  }

  get isEditable() {
    return  this.access.hasRole('superuser');
  }
}
