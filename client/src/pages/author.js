import {inject, bindable, computedFrom, LogManager} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {rewriteURLParam} from 'lib/utils';
import {Access} from 'lib/access';
import {Router} from 'aurelia-router';

const logger = LogManager.getLogger('author');

@inject(ApiClient, Access, Router)
export class Author {
  _loader;
  @bindable filter;
  author;

  constructor(client, access, router) {
    this.client=client;
    this.access = access;
    this.router = router;
  }

  activate(params, route)  {
    logger.debug('Author activated with '+JSON.stringify(params));
    this.id=params.id;
    this.client.getOne('authors', params.id)
    .then(data => {
      this.author=data;
      route.navModel.setTitle(`Author ${this.author.first_name?this.author.first_name+' ':''}${this.author.last_name}`);
      logger.debug('Loaded author'+JSON.stringify(data));
      })
    .catch(err => logger.error(`Fetch error ${err}`, err));
    if (params.filter) this.filter=params.filter;

    this.updateLoader()
  }

  filterChanged() {
    logger.debug('Filter changed to '+ this.filter);
    rewriteURLParam('filter', this.filter);
    this.updateLoader()
  }

  updateLoader() {
    this._loader = this.client.authorBooks.bind(this.client, this.id, this.filter);
  }

  @computedFrom('_loader')
  get loader() {
    return this._loader;
  }

  get editActions() {
    return [{text:"Information",value:'edit', icon:'info-circle'},
      {text:'Merge', value:'merge', icon:'compress'}];

  }

  get editAction() {
    return action => {
    switch (action) {
      case 'edit':
        this.router.navigateToRoute('author-edit', {id:this.author.id})
      break;
      case 'merge':
      this.router.navigateToRoute('author-merge', {id: this.author.id});
      break;
    }
  }
  }

  get isEditable() {
    return  this.access.hasRole('superuser');
  }

}
