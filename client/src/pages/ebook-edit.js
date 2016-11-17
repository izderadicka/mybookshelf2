import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router, activationStrategy} from 'aurelia-router';
import $ from 'jquery';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';
import {Ebook} from 'models/ebook';
import {DialogService} from 'aurelia-dialog';
import {Edit} from './abstract/edit';

let logger = LogManager.getLogger('ebook-edit')

@inject(ApiClient, Router, Access, DialogService)
export class EditEbook extends Edit{
  ebook;
  originalEbook;
  _languages;
  _genres;
  @bindable _series;
  _seriesSelected;

  constructor(client, router, access, dialog) {
    super(client, router, access, dialog);
    this.viewRoute = 'ebook';
    this.modelEntity = 'ebooks';
  }

/*
 * It does not help with pagination back problem

  determineActivationStrategy(){
    return activationStrategy.replace;
    //return activationStrategy.invokeLifecycle;
  }
*/

  canActivate(params) {
    if (params.id !== undefined) {
    return this.client.getOne('ebooks', params.id)
      .then(b => {
        this.ebook=new Ebook(b);
        this.model=this.ebook;
        this._series = b.series ? b.series.title : undefined;
        logger.debug(`Ebook data ${JSON.stringify(b)}`);
        return this.access.canEdit(b.created_by);
      })
      .catch(err => { logger.error(`Failed to load ${err}`);
                      return false;})

    } else {
      this.ebook = new Ebook();
      this.model = this.ebook;
      this._series = undefined;
      return true;
    }

  }
  activate(params) {
    logger.debug(`Activated with ${JSON.stringify(params)}`)
    let promises = [];

    promises.push(
    this.client.getManyUnpagedCached('languages')
      .then( data => {
      this._languages = data;
      logger.debug(`Got languages ${JSON.stringify(this._languages)}`)
      }
      ),
    this.client.getManyUnpagedCached('genres')
      .then(data => this._genres = data)
    );

    if (params.upload) {
      promises.push(
          this.client.getOne('uploads-meta', params.upload)
          .then(upload=> {
            this.uploadId=upload.id;
            this.meta = upload.meta;
          })
          .catch(err=> logger.error('Upload fetch error: '+err))
      )
    }

    return Promise.all(promises).then(() => {
      logger.debug('Try to use metada '+ JSON.stringify(this.meta));
      if (this.meta) this.prefill()});
  }


  prefill() {
    if (this.meta.title) this.ebook.title = this.meta.title;
    if (this.meta.authors && this.meta.authors.length) {
      this.ebook.authors=this.meta.authors;
    }
    if (this.meta.series && this.meta.series.title) {
      this.ebook.series =  this.meta.series;
      this._series = this.meta.series.title;
      this.ebook.series_index = this.meta.series_index;
    }

    if (this.meta.language && this.meta.language.id) {
      this.ebook.language = {id:this.meta.language.id};
    }

    if (this.meta.genres && this.meta.genres.length) {
      this.ebook.genres = this.meta.genres.filter(i => i.id);
    }
  }

  _seriesChanged() {
    logger.debug(`Series is ${this._series} selected ${JSON.stringify(this._seriesSelected)}`);
    if (this._seriesSelected) this.ebook.series = this._seriesSelected
    else this.ebook.series = {title: this._series};
  }

  save() {
    //logger.debug(`Saving ${JSON.stringify(this.ebook)}`);
    this.error=undefined;

    if (this.validate()) {
      let data = this.ebook.prepareData();
      if (!data || ! Object.keys(data).length) {
        this.error={error:'No changes to save'};
        return
      }
      let result;
      if (this.ebook.id) {
        result = this.client.patch('ebooks', data, this.ebook.id)
      } else {
        result = this.client.post('ebooks', data);
      }

      result.then(res => {
        if (res.error) {
          this.error={error:res.error, errorDetail:res.error_details}
        } else if (res.id) {
          let action = this.uploadId ? this.client.addUploadToEbook(res.id, this.uploadId, this.meta.quality || null) : Promise.resolve({})
           action.then(res2 => {
              if (res2.error) this.error = {
                error: res2.error,
                errorDetail: res2.error_details }
              else
                this.router.navigateToRoute('ebook', {id:res.id});
              })
            .catch(err => this.error={error:"Server error attaching source", errorDetail:err});

        } else {
          this.error = {error:'Invalid respose', errorDetail: 'Ebook ID is missing'}
        }
      })
      .catch(err => this.error={error:'Request failed', errorDetail:err})


    } else {
      logger.debug(`Validation fails`)
    }
  }

  afterSave() {
    let action = this.uploadId ? this.client.addUploadToEbook(res.id, this.uploadId, this.meta.quality || null) : Promise.resolve({})
     action.then(res2 => {
        if (res2.error)
          throw new Error(`Cannot add upload to this ebook: ${res2.error}, ${res2.error_details}`)
        else
          this.router.navigateToRoute('ebook', {id:res.id});
        })
  }


  get seriesLoader() {
    return start => this.client.getIndex('series', start);
  }

  get deleteConfirmMessage() {
    return `Do you want to delete ebook ${this.ebook.title}?`;
  }

}
