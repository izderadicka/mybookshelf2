import {inject, bindable, LogManager} from 'aurelia-framework';
import {HttpClient} from 'aurelia-fetch-client';
import $ from 'jquery';

const logger=LogManager.getLogger('ebook-card');

@inject(HttpClient)
export class EbookCard {
  @bindable ebook;
  @bindable description;
  @bindable editAction;
  @bindable deleteAction;
  @bindable reloadAction;

  constructor(http) {
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

  delete(evt) {
    if (this.deleteAction) {
      this.deleteAction(evt)
      .then( () => {
      if (this.reloadAction) this.reloadAction();
    });
    }
  }

  edit(evt) {
    if (this.editAction) {
      this.editAction(evt)
      .then( (res) => {
        if (this.reloadAction && res !== 'noreload') this.reloadAction();
      })

    }
  }

}
