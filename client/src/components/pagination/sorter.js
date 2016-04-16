import {
  bindable,
  LogManager
} from 'aurelia-framework';
const logger = LogManager.getLogger('sorter');

export class sorter {
  @bindable sort;
  @bindable sortings;

  constructor() {
    if (history.state) {
      const state = history.state;
      logger.debug('restoring sorter back to ' + JSON.stringify(state));
      if (state.sort) {
        this.sort = state.sort;
        logger.debug(`sort is ${this.sort}`);
      }
    }
  }

}
