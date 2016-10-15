import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {ConfirmDialog} from 'components/confirm-dialog';
import {DialogService} from 'aurelia-dialog';

let logger = LogManager.getLogger('ebook-merge');

@inject(ApiClient, Router, Access, DialogService)
export class EbookMerge {
  constructor(client, router, access, dialog) {
    this.client = client;
    this.router = router;
    this.access = access;
    this.dialog = dialog;

    this.mergeTo = true;
  }

  canActivate(params) {
    if (! params.id) return false;
    return this.client.getOne('ebooks', params.id)
    .then( b=> {
      this.ebook=b
      return true})
    .catch(err => {
      logger.error(`Ebook fetch error: ${err}`);
      return false;
    })
  }

  get loaderEbooks() {
    return start => this.client.getIndex('ebooks', start);
  }

  get ready() {
    return this.ebook.id && this.otherEbook && this.otherEbook.id;
  }

  cancel() {
    this.router.navigateToRoute('ebook', {id: this.ebook.id});
  }

  merge() {
    this.error=null;
    if (this.ebook && this.otherEbook) {
      let promise= this.mergeTo? this.client.mergeEbooks(this.otherEbook.id, this.ebook.id):
                                this.client.mergeEbooks(this.ebook.id, this.otherEbook.id);
      promise.then(res => this.router.navigateToRoute('ebook', {id: res.id}))
      .catch(err => {
        logger.error('Error in ebooks merge', err);
        this.error={error:'Server Error', errorDetail:err};
      });
  }
}
}
