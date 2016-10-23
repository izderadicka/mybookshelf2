import {inject, bindable} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {rewriteURLParam} from 'lib/utils';

const logger = LogManager.getLogger('welcome');

@inject(ApiClient)
export class Welcome {

  constructor(client) {
    this.client = client;
  }

  activate() {
  
  }



}
