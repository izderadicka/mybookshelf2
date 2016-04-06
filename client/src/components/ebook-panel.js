
import {inject, bindable, LogManager} from 'aurelia-framework';
const logger=LogManager.getLogger('ebooks-panel');

export class EbookPanel {
  @bindable sortings=[{name:'Title A-Z', key:'title'}, {name:'Title Z-A',key:'-title'}];
  @bindable loader;

  loaderChanged() {
    logger.debug('Loader changed in EbookPanel');
  }
}
