import {inject, bindable, LogManager} from 'aurelia-framework';
import {HttpClient} from 'aurelia-fetch-client';
import $ from 'jquery';
import {BaseCard} from './base-card';

const logger=LogManager.getLogger('ebook-card');

@inject(HttpClient)
export class EbookCard extends BaseCard{
  @bindable ebook;
  @bindable description;
  @bindable editAction;
  @bindable deleteAction;
  @bindable reloadAction;

  constructor(http) {
    super();
    this.http=http;
  }

  handleImgError(evt) {
      logger.debug('Missing thumb');
      $(evt.target).parent().addClass('missing');

  }

  handleImgLoad(evt) {
      logger.debug('Load thumb');
      $(evt.target).parent().removeClass('missing');

  }

  getThumbSource(ebook) {
    return this.http.baseUrl +'/thumb/'+ebook.id;
  }


}
