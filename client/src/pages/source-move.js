import {inject, LogManager} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {DialogController} from 'aurelia-dialog';

const logger = LogManager.getLogger('source-move');

@inject(ApiClient, Router, Access, DialogController)
export class SourceMove {

  constructor(client, router, access, controller) {
    this.client = client;
    this.router = router;
    this.access = access;
    this.controller = controller;
    this.controller.settings.lock = true;
  }

  canActivate(params) {
    if (! params.ebookId) return false;
    return this.client.getOne('ebooks', params.ebookId)
    .then( b=> {
      this.ebook=b;
      if  (!this.access.canEdit(b.created_by)) return false;

      for (let source of this.ebook.sources) {
        if (source.id == params.sourceId) {
          this.source =source;
          return this.access.canEdit(source.created_by);
        }
      }
      return false;
      })
    .catch(err => {
      logger.error(`Ebook fetch error: ${err}`);
      return false;
    })
  }

  get ready() {
    return this.ebook && this.otherEbook && this.otherEbook.id;
  }

  get loader() {
    return start => this.client.getIndex('ebooks', start);
  }

  get filterOutThisEbook() {
    return b => b.id !== this.ebook.id;
  }
}
