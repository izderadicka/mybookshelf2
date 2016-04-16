import {inject,DOM, bindable} from 'aurelia-framework'
import {LogManager} from 'aurelia-framework';
const logger = LogManager.getLogger('pager');

@inject(DOM.Element)
export class Pager{
  @bindable page;
  @bindable lastPage;
  @bindable loading = false;

  constructor(elem) {
    this.elem=elem;
  }

  activated() {
    logger.debug('Pager activated');
  }

  nextPage() {
    if (this.page < this.lastPage && ! this.loading) this.page++;
  }

  prevPage() {
    if (this.page >1 && ! this.loading) this.page--;
  }

  get nextPageNo() {
    return Math.min(this.lastPage, this.page+1)
  }

  get prevPageNo() {
    return Math.max(this.page-1, 1)
  }

  get isFirstPage() {
    return this.page===1
  }

  get isLastPage() {
    return this.page === this.lastPage || ! this.lastPage
  }
}
