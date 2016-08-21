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
  ebookCandidates=[];
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
      this.client.getCoverMeta(model.id)
        .then(blob => this.cover.src = URL.createObjectURL(blob))

      return meta.meta
    })
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
      return true;
      })
    .catch(err => {
      logger.error(`Upload meta error ${err}`);
      return false});

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

  addToEbook(ebookId) {
    this.client.addUploadToEbook(ebookId, this.id)
    .then(res => {
      if (res.error) this.error={error:res.error, errorDetail:res.error_details}
      else {
        this.router.navigateToRoute('ebook', {id:ebookId});
      }
    })
    .catch(err => this.error={error:'Server error', errorDetail:err})
  }

}
