import {inject} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Merge} from './abstract/merge';

@inject(ApiClient, Router, Access)
export class AuthorMerge extends Merge{
  constructor(client, router, access) {
    super(client, router, access);
    this.viewRoute = 'author';
    this.modelEntity = 'authors';
  }

  canMerge() {
    return this.access.hasRole('superuser');
  }

  getFullName(item) {
    let name= item.first_name ? item.last_name + ', ' + item.first_name : item.last_name
    //if (!item.id) name+= ' (new)';
    return name
  }

}
