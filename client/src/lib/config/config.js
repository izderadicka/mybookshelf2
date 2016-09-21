import {
  inject,
  LogManager
} from 'aurelia-framework';

let logger = LogManager.getLogger('config');

export class Configure {

  constructor() {
    this._config = {};
  }

  configure(val) {
    this._config = val;
  }

  get(key, defval = undefined) {
    var parent = this._config;
    for (var k of key.split('.')) {
      if (parent.hasOwnProperty(k) && parent[k]) {
        parent = parent[k];
      } else {
        return defval;
      };
    }
    return parent;
  }

}
