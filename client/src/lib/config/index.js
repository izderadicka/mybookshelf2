import {Configure} from './config';
import {LogManager} from 'aurelia-framework';

let logger=LogManager.getLogger('config');

export function configure(aurelia, cb) {
  logger.debug('Calling configure method')
  let instance= aurelia.container.get(Configure);
  if (cb && typeof cb=='function') {
    cb(instance);
  }
}

export {Configure}
