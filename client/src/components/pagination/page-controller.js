import {bindable, processContent, noView, inject, customElement, computedFrom} from 'aurelia-framework'
import {LogManager} from 'aurelia-framework';
const logger = LogManager.getLogger('page-controller');

@noView()
@processContent(false)
@customElement('page-controller')
export class PageController {
  @bindable page=1;
  @bindable sort;
  lastPage;
  @bindable pageSize = 10;
  loading=false;
  data=[];
  @bindable loader = () => Promise.reject(new Error('No loader specified!'));
  @bindable noSort=false;

  constructor() {
    logger.debug('Constructing PageContoller - history state is ' + JSON.stringify(history.state));

    if (history.state) {
      const state=history.state;
      logger.debug('restoring page-controller back to '+JSON.stringify(state));
      if (state.page && state.page != this.page) {
        this.page=state.page;
      }
      if (state.sort) {
        this.sort=state.sort;
        logger.debug(`sort2 is ${this.sort}`);
      }
    }
    }

  created(owningView, myView) {
    logger.debug('Creating PageController');
  }
  bind(ctx) {
    logger.debug(`Binding PageController`);
    // if status is restored from history change to page will not happen so we need to load page here
    if (history.state && history.state.page || this.noSort) this.loadPage(this.page);

  }
  attached() {
    logger.debug('PageController attached');
  }

  loadPage(page, unbinded=false) {
    //if (! this.loader) return Promise.resolve(null);
    logger.debug(`Loading page ${page}, ${this.sort} by ${this.loader.name}`);
    this.loading=true;
    this.error=null;
    return this.loader(page, this.pageSize, this.sort)
      .then(({data,lastPage}) => { this.data=data;
                                this.lastPage=lastPage },
            err => {
              logger.error(`Page Load Error: ${err}`);
              this.error={error:'Page Load Error', errorDetail:err};
            })
      .then(() => this.loading=false);
  }

  get reloadPage() {
    return (wasDelete) => {
      if (this.data && this.data.length ===1 && wasDelete && this.page>1) {
        this.page=this.page-1;
      } else {
        this.loadPage(this.page);
      }
    }
  }

  pageChanged(newPage) {
    logger.debug('page changed '+newPage);
    this.loadPage(this.page)
    .then(() => {history.replaceState({...(history.state || {}), page:this.page, sort:this.sort}, '')});
  }

  sortChanged(newValue, old) {
    logger.debug(`sort changed ${this.sort}`);
    this.reset();

  }

  loaderChanged() {
    logger.debug('Loader changed in PageController');
    this.reset();
  }

  reset() {
    const oldPage=this.page;
    this.page=1;
    if (oldPage==1) this.pageChanged(1,1);
  }

  @computedFrom('data', 'loader')
  get empty() {
    return ! this.data || this.data.length==0;
  }

}
