import {inject} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {LogManager} from 'aurelia-framework';
import {Access} from 'lib/access';
import {DialogService} from 'aurelia-dialog';
import {ConfirmDialog} from 'components/confirm-dialog';

let logger = LogManager.getLogger('ebooks');

@inject(ApiClient, Access, DialogService)
export class Ebook {
  ebook
  constructor(client, access, dialog ) {
    this.client=client;
    this.access=access;
    this.dialog =  dialog;
    this.token = access.token;
    this.canDownload=access.hasRole('user');
    this.canConvert=access.hasRole('user');
    this.cover = new Image();
    this.cover.onload = function() {
        URL.revokeObjectURL(this.src);
      }
  }


  get isEditable() {
    return this.ebook && this.access.canEdit(this.ebook.created_by);
  }

  canActivate(params) {
    return this.client.getOne('ebooks', params.id)
      .then(b => {
        this.ebook=b;
        return this.client.getCover('ebooks', b.id)
          .then (blob => {
            this.cover.src = URL.createObjectURL(blob);
            return true })
          .catch(err => {
            logger.warn(`Cannot load cover for ebook ${b.id}: ${err}`);
            return true
          })
        return true;})
      .catch(err => {
        logger.error(`Failed to load ${err}`);
        return false;
      });
  }

  attached() {
    if (this.cover.src)
      document.getElementById('cover-holder').appendChild(this.cover);
  }

  canDeleteSource(source) {
    return this.access.canEdit(source.created_by);
  }

  deleteSource(source) {
    this.dialog.open({
        viewModel: ConfirmDialog,
        model: {
          action: 'Delete',
          message: `Do you want to delete ${source.format} file from ebook ${this.ebook.title}?`
        }
      })
      .then(resp => {
        if (!resp.wasCancelled) {
        this.client.delete('sources', source.id)
          .then(res => {
            if (res.error) {
              logger.error('Source delete failed: ' + res.err);
            } else {
              let idx = this.ebook.sources.findIndex(x => x === source)
              if (idx >= 0) this.ebook.sources.splice(idx, 1);
            }
          })
          .catch(err => {
            logger.error('Server error: ' + err);
          })
        }
      });
  }

}
