import {
  inject,
  LogManager,
  Loader
} from 'aurelia-framework';

let logger = LogManager.getLogger('config');

@inject(Loader)
export class Configure {
  _config = null;
  constructor(loader) {
    this.loader = loader;
  }

  loadFile() {
    return this.loader.loadText(`config/config.json`)
      .then(txt => {
        let data = JSON.parse(txt);
        this._config = data;
        logger.debug('Loaded my config file');
      })
      .catch((err) => reject(new Error(`Error loading config ${err}`)))
  }

  get(key, defval = undefined) {
    var parent = this._config;
    for (var k of key.split('.')) {
      if (parent.hasOwnProperty(k)) {
        parent = parent[k];
      } else {
        return defval;
      };
    }
    return parent;
  }

}
