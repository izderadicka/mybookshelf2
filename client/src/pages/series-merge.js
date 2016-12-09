import {inject} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Merge} from './abstract/merge';

@inject(ApiClient, Router, Access)
export class Series extends Merge{
  constructor(client, router, access) {
    super(client, router, access);
    this.viewRoute = 'series';
    this.modelEntity = 'series';
  }

  canMerge() {
    return this.access.hasRole('superuser');
  }

}
