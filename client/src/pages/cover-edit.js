import {inject, LogManager, computedFrom} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import {WSClient} from 'lib/ws-client';
import {Router} from 'aurelia-router';
import {EventAggregator} from 'aurelia-event-aggregator';
import $ from 'jquery';

const logger = LogManager.getLogger('cover-edit');

@inject(Element, ApiClient, WSClient, Router, EventAggregator)
export class CoverEdit {
  constructor(elem, client, wsClient, router, event) {
    this.elem = elem;
    this.client = client;
    this.router = router;
    this.wsClient = wsClient;
    this.event = event;
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

  showFile() {
    this.fileOK = false;
    let files=document.getElementById('file-input');
    if (files.files.length) {
      let reader = new FileReader();
      let file = files.files[0];
      if (! /^image\//.test(file.type)) return;
      let promise= new Promise(
       (resolve, reject) => {
      reader.onload = (evt) => {
        resolve(evt.target.result);
        this.fileOK = true;
      }});
      reader.readAsDataURL(file);
      this.coverLoader = promise;
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
            this.event.subscribe('cover-ready', result =>{
              if (taskId == result.taskId) {
                this.uploading=false;
                this.router.navigateToRoute('ebook', {id: this.ebook.id});
              }
            });
            this.event.subscribe('cover-error', result => {
              if (taskId == result.taskId) {
                this.setError('Cover resize error', result.error);
              }
            });

          })
          .catch(err => this.setError('WS error', err));
        }
      })
      .catch(err => this.setError('Upload error', err));
  }

  cancel() {
    this.router.navigateToRoute('ebook', {id:this.ebook.id});
  }
}
