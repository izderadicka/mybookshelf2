import {inject, bindable, LogManager} from 'aurelia-framework';
import {HttpClient} from 'aurelia-fetch-client';
import {ApiClient} from 'lib/api-client';
import {AuthorsValueConverter} from 'components/authors-converter';
import $ from 'jquery';

const logger=LogManager.getLogger('ebooks-tiles');

@inject(HttpClient, ApiClient, Element)
export class EbookTiles {
  @bindable mininum=10;

  constructor(http, client, elem) {
    this.http=http;
    this.client=client;
    this.conv = new AuthorsValueConverter();
    this.elem = elem;
  }

  attached() {
    this.container = $('.ebook-tiles', this.elem);
    this.countNumber();
    this._resize_handler = (evt) => {
      if (this._resizeFuture) clearTimeout(this._resizeFuture);
      this._resizeFuture = setTimeout(() => this.countNumber(), 300)
    }
    $(window).resize(this._resize_handler);
  }

  detached() {
    $(window).unbind('resize', this._resize_handler);
  }

  loadEbooks(page, size, need) {
    this.client.getMany('ebooks', page, size, '-created')
    .then(res => {
      this.lastPage = res.lastPage;
      if (need && this.ebooks && this.ebooks.length < need) {
        this.ebooks = this.ebooks.concat(res.data.slice(0, need - this.ebooks.length));
      } else {
      this.ebooks=res.data;
    }

    })
    .catch(err => logger.error('Fetch error', err));
  }

  calcNeed() {
    let columns = Math.floor(this.container.width() / 100);
    let need = Math.ceil(this.mininum / columns) * columns;
    logger.debug(`Need = ${need}`);
    return need;
  }
  countNumber() {
    let need = this.calcNeed()
    if (! this.ebooks ) {
      this.loadEbooks(1, need);
    } else if (this.ebooks.length > need) {
      this.ebooks = this.ebooks.slice(0, need);
    } else if (this.ebooks.length < need && this.lastPage > 1) {
      this.loadEbooks(2, this.ebooks.length, need)
    }

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

  reload() {
    let sz = this.calcNeed();
    this.loadEbooks(1,sz);
  }
}
