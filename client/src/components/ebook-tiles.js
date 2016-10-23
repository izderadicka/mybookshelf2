import {inject, bindable, LogManager} from 'aurelia-framework';
import {HttpClient} from 'aurelia-fetch-client';
import {AuthorsValueConverter} from 'components/authors-converter';
import $ from 'jquery';

const logger=LogManager.getLogger('ebooks-tiles');

@inject(HttpClient)
export class EbookTiles {
  @bindable ebooks

  constructor(http) {
    this.http=http;
    this.conv = new AuthorsValueConverter();
  }

  handleImgError(evt) {
      logger.debug('Missing thumb');
      $(evt.target).parent().addClass('missing');

  }

  handleImgLoad(evt) {
      logger.debug('Load thumb');
      $(evt.target).parent().removeClass('missing');

  }

  getFullTitle(ebook) {
    if (ebook.authors && ebook.authors.length) {
      let authors = this.conv.toView(ebook.authors.slice(0, 2));
      return `${ebook.title} by ${authors}`;
    } else {
    return ebook.title;
    }
  }

  getThumbSource(ebook) {
    return this.http.baseUrl +'/thumb/'+ebook.id;
  }
}
