import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
let logger = LogManager.getLogger('ebooks');

@inject(ApiClient)
export class Ebooks {
  sortings=[{name:'Title A-Z', key:'title'}, {name:'Title Z-A',key:'-title'}];
  constructor(client) {
    this.client=client
  }
  activate(params) {
    logger.debug(`History State ${JSON.stringify(history.state)}`);
  }

  get loader() {
    return this.client.getMany.bind(this.client, 'ebooks');
  }

}
