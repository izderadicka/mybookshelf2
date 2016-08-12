import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {Router} from 'aurelia-router';

let logger = LogManager.getLogger('upload-result');

@inject(ApiClient, Router)
export class UploadResult {
  meta;
  metaId;
  file;
  ebook;
  ebookCandidates=[];
  cover=new Image();
  constructor(client, router) {
    this.client=client;
    this.router = router;
    // has to revoke object URL to release blob
    this.cover.onload = function() {
        URL.revokeObjectURL(this.src);
      }

  }

  activate(model) {
    logger.debug(`Activated with ${JSON.stringify(model)}`);
    this.client.getOne('uploads-meta', model.id)
    .then(meta => {
      this.meta = meta.meta;
      this.metaId = meta.id;
      this.file = meta.load_source;
      logger.debug(`Got meta ${JSON.stringify(meta)}`);
      this.client.getCoverMeta(model.id)
        .then(blob => this.cover.src = URL.createObjectURL(blob))

      return meta.meta
    })
    .catch(err => logger.error(`Upload meta error ${err}`))
    .then(meta => {
      var authors = meta.authors ? meta.authors.join(' ') : null;
      var search=meta.title ? meta.title : '';
      search = meta.series ? search + ' '+ meta.series : search
      search = authors ? authors + ' ' + search : search;
      logger.debug(`Searching for ebooks: ${search}`);
      return this.client.search(search, 1, 5);
      })
    .then(result => {
      logger.debug(`Found ${result.data}`);
      this.ebookCandidates=result.data;

      })

  }

  attached() {
    document.getElementById('cover-holder').appendChild(this.cover);
  }

  @computedFrom('ebookCandidates')
  get hasCandidates() {
    return this.ebookCandidates && this.ebookCandidates.length>0;
  }

  createNew() {
    this.router.navigateToRoute('ebook-create', {metaId: this.metaId});
  }

}
