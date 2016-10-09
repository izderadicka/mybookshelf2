import {LogManager, inject} from 'aurelia-framework';
import {Configure} from 'lib/config/index';

let log = LogManager.getLogger('date-converter');

@inject(Configure)
export class DateValueConverter {

  constructor(config) {
    this.config = config;
  }
  toView(val) {
    try {
      let date = new Date(val);
      let locale = this.config.get('locale');
      return date.toLocaleString(locale)
      return
    } catch (error) {
      log.error(`Date formating error: ${error}`, val)
      return val;
    }
  }
}
