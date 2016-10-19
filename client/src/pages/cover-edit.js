import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {WSClient} from 'lib/ws-client';
import {Router} from 'aurelia-router';
import $ from 'jquery';

const logger = LogManager.getLogger('cover-edit');

@inject(Element, ApiClient, WSClient, Router)
export class CoverEdit {
  constructor(elem, client, wsClient, router) {
    this.elem = elem;
    this.client = client;
    this.router = router;
    this.wsClient = wsClient;

    this.cover=new Image();
    this.cover.onload = function() {
        URL.revokeObjectURL(this.src);
      }
  }

  canActivate(params) {
    if (! params.id) return false;
    return this.client.getOne('ebooks', params.id)
    .then( b=> {
      this.ebook=b;
      if (b.cover) {
      this.coverLoader= this.client.getCover('ebooks', b.id);
      }
      return true;
      })
    .catch(err => {
      logger.error(`Ebook fetch error: ${err}`);
      return false;
    })
  }

  attached() {
    $('#cover-holder', this.elem).append(this.cover);
    if (this.coverLoader)
      this.coverLoader.then(blob => {
        this.cover.src = URL.createObjectURL(blob);

      })
      .catch(err => {
        logger.warn(`Cannot load cover for upload ${this.ebook.title}: ${err}`);
      });
  }

  showFile() {
    this.fileOK = false;
    let files=document.getElementById('file-input');
    if (files.files.length) {
      let reader = new FileReader();
      let file = files.files[0];
      if (! /^image\//.test(file.type)) return;
      reader.onload = (evt) => {
        this.cover.src=evt.target.result;
        this.fileOK = true;
      }
      reader.readAsDataURL(file);
    }
  }

  setError(txt, err) {
    let msg=txt+' '+err;
    this.error={error:txt, errorDetail:err};
    logger.error(msg);
    this.uploading = false;
  }

  uploadCover() {
    this.uploading = true;
    let formData= new FormData($('#file-upload-form', this.elem)[0]);
    this.client.upload(formData, 'upload-cover')
      .then(data => {
        if (data.error) {
          this.setError('Upload error:',data.error);
        } else {
          logger.debug(`File uploaded ${JSON.stringify(data)}`);
          this.wsClient.changeCover(data.file, this.ebook)
          .then(taskId => {
            logger.debug('Cover update send as task '+taskId);
          })
        }
      })
      .catch(err => this.setError('Upload error', err));
  }

  cancel() {
    this.router.navigateToRoute('ebook', {id:this.ebook.id});
  }
}
