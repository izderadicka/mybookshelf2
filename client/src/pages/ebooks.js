import {inject, bindable} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {rewriteURLParam} from 'lib/utils';
let logger = LogManager.getLogger('ebooks');

@inject(ApiClient)
export class Ebooks {
  @bindable genres

  constructor(client) {
    this.client=client
  }
  activate(params) {
    logger.debug(`History State ${JSON.stringify(history.state)}`);
    if (params.genres) {
    this.genres = params.genres.split(',');
    }
    this.updateLoader()

  }

  updateLoader() {
    this._loader = (page, pageSize, sort) => {
      return this.client.getMany('ebooks', page, pageSize, sort,
      this.genres && this.genres.length? {genres: this.genres.join(',')}:undefined);
    }
    rewriteURLParam('genres', this.genres? this.genres.join(','):null);
  }

  genresChanged() {
    logger.debug('genres changed to '+ this.genres);
    this.updateLoader();
  }


  get loader() {
    return this._loader;
  }

}
