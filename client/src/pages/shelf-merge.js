import {inject} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Merge} from './abstract/merge';

@inject(ApiClient, Router, Access)
export class EbookMerge extends Merge{
  constructor(client, router, access) {
    super(client, router, access);
    this.viewRoute = 'shelf';
    this.modelEntity = 'bookshelves';
  }

  get loader() {
    return start => this.client.getIndex(this.modelEntity+'/mine', start);
  }

}
