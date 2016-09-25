import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {Router} from 'aurelia-router';

let logger = LogManager.getLogger('upload-result');

@inject(ApiClient, Router)
export class UploadResult {
  meta;
  metaId;
  id;
  file;
  ebook;
  ebooksCandidates;
  ebooksSearched;
  cover=new Image();
  error;
  constructor(client, router) {
    this.client=client;
    this.router = router;
    // has to revoke object URL to release blob
    this.cover.onload = function() {
        URL.revokeObjectURL(this.src);
      }

  }

  canActivate(model) {
    logger.debug(`Activated with ${JSON.stringify(model)}`);
    this.id = model.id;
    return this.client.getOne('uploads-meta', model.id)
    .then(meta => {
      this.meta = meta.meta;
      this.metaId = meta.id;
      this.file = meta.load_source;
      logger.debug(`Got meta ${JSON.stringify(meta)}`);
      if (meta.cover) {
      this.client.getCover('uploads-meta', model.id)
        .then(blob => this.cover.src = URL.createObjectURL(blob))
      }
      return meta.meta
    })
    .then(meta => {
      var authors = meta.authors ? meta.authors.map(a => a.first_name ? a.first_name + ' ' + a.last_name : a.last_name ).join(' ') : null;
      var search=meta.title ? meta.title : '';
      search = meta.series ? search + ' '+ meta.series.title : search
      search = authors ? authors + ' ' + search : search;
      logger.debug(`Searching for ebooks: ${search}`);
      return this.client.search(search, 1, 5).
        catch(err => {
          logger.error('Search failed: '+err);
          return {};
        });
      })
    .then(result => {
      logger.debug(`Found ${result.data}`);
      if (result.data && result.data.length) this.ebooksCandidates=result;
      return true;
      })
    .catch(err => {
      logger.error(`Upload meta error ${err}`);
      return false});

  }

  attached() {
    if (this.cover.src)
      document.getElementById('cover-holder').appendChild(this.cover);
  }

  createNew() {
    this.router.navigateToRoute('ebook-create', {upload: this.id});
  }

get addToEbook() {
  return ebookId => {
    this.client.addUploadToEbook(ebookId, this.id, this.meta.quality || null)
      .then(res => {
        if (res.error) this.error = {
          error: res.error,
          errorDetail: res.error_details
        }
        else {
          this.router.navigateToRoute('ebook', {
            id: ebookId
          });
        }
      })
      .catch(err => this.error = {
        error: 'Server error',
        errorDetail: err
      });
  }
}

get search() {
  return ({query}) => {
    this.ebooksSearched = null;
    this.client.search(query, 1, 5)
    .then(res => {
      this.ebooksSearched = res;

    })
    .catch(err => this.error ={error: 'Search error', errorDetail:err});
  }
}

}
