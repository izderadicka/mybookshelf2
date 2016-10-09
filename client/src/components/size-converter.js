import {LogManager, inject} from 'aurelia-framework';
import {Configure} from 'lib/config/index';

let log = LogManager.getLogger('size-converter');

let sufixes = ['B', 'kB', 'MB', 'GB', 'TB']

@inject(Configure)
export class SizeValueConverter {

  constructor(config) {
    this.config = config;
  }

  toView(val, decimals=1) {
    let index = 0;
    while (val >=1024 && index < sufixes.length) {
      val = val/1024;
      index++;
    }
    let exp = 10**decimals;
    val=Math.round(val*exp)/exp;
    let locale = this.config.get('locale');
    try {
      val=val.toLocaleString(locale);
    } catch (err) {
      log.error('Size formating error: '+err);
    }
    return `${val} ${sufixes[index]}`;
  }
}
