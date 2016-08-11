import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router, activationStrategy} from 'aurelia-router';
import $ from 'jquery';
import {ApiClient} from 'lib/api-client';
import {Access} from 'lib/access';

let logger = LogManager.getLogger('ebook-edit')

@inject(ApiClient, Router, Access)
export class EditEbook {
  ebook;
  originalEbook;
  _languages;
  _genres;
  @bindable _series;
  _seriesSelected;

  constructor(client, router, access) {
    this.client = client;
    this.router = router;
    this.access = access;
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
        this.ebook=b;
        this.originalEbook=JSON.parse(JSON.stringify(b)); // deep copy of b
        this._series = b.series ? b.series.title : undefined;
        logger.debug(`Ebook data ${JSON.stringify(b)}`);
        return this.access.canEdit(b.id);
      })
      .catch(err => logger.error(`Failed to load ${err}`));
    } else {
      this.ebook = {authors:[], genres:[]};
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
    return Promise.all(promises);
  }

  _seriesChanged() {
    logger.debug(`Series is ${this._series} selected ${JSON.stringify(this._seriesSelected)}`);
    if (this._seriesSelected) this.ebook.series = this._seriesSelected
    else this.ebook.series = {title: this._series};
  }

  save() {
    logger.debug(`Saving ${JSON.stringify(this.ebook)}`);
    if (this.validate()) {
      this.prepareData();
    } else {
      logger.debug(`Validation fails`)
    }
  }


  prepareData() {
    let data = {}
    let isNew = ! this.originalEbook;

    let shrink = function(obj) {
      if  (!obj) return null;
      if (obj.hasOwnProperty('id') && obj.id) {
        return {id:obj.id}
      } else {
        let newObj = {}
        for (var prop of Object.keys(obj)) {
          if (prop !=='id' && obj[prop]) newObj[prop] = obj[prop]
        }
        if (Object.keys(newObj).length === 0) return null;
        return newObj;
      }
    };

      let shrinkList = function(l) {
        if (!l) return [];
        return l.map(shrink).filter(x => x);
      }

      let compareObjects = function(o1, o2) {
        return JSON.stringify(o1) === JSON.stringify(o2);
      }
        // delete all except
    if (isNew || this.ebook.title !== this.originalEbook.title) data.title = this.ebook.title;
    if (isNew || this.ebook.language.id !== this.originalEbook.language.id)
      data.language = shrink(this.ebook.language);

    if (isNew || this.ebook.series_index != this.originalEbook.series_index) data.series_index = this.ebook.series_index;

    let newSeries = shrink(this.ebook.series)
    if (isNew || ! compareObjects(newSeries, shrink(this.originalEbook.series)))
      data.series = newSeries;

    let newAuthors = shrinkList(this.ebook.authors);
    if (isNew || ! compareObjects(newAuthors, shrinkList(this.originalEbook.authors)))
      data.authors = newAuthors;

    let newGenres =  shrinkList(this.ebook.genres)
    if (isNew || ! compareObjects(newGenres, shrinkList(this.originalEbook.genres)))
      data.genres = newGenres;



    if (! isNew && Object.keys(data).length) {
      data.id = this.ebook.id;
      data.version_id = this.ebook.version_id;
    }

    logger.debug(`New data : ${JSON.stringify(data)}`);
    return data;

  }
  validate() {
    $('.has-error').removeClass('has-error');
    $('.help-block').remove();
    let errors = [];

    let addError = function (what,err) {
      errors.push(err);
      let grp=$(`#${what}-input-group`);
      grp.addClass('has-error');
      $('<span>').addClass('help-block').text(err).appendTo(grp);

    }
    // Title
    if (!this.ebook.title) addError('title', 'Title is mandatory!');
    if (this.ebook.title && this.ebook.title.length > 256) addError('title', 'Title too long');
    // Language
    if ( !this.ebook.language || !this.ebook.language.id) addError('language', 'Language is mandatory');
    // Series
    if ( this.ebook.series && this.ebook.series.title && ! this.ebook.series_index)
      addError('series', 'If series title is present then series index is mandatory');
    if ( !(this.ebook.series && this.ebook.series.title) &&  this.ebook.series_index)
      addError('series', 'If series index is present then series title is mandatory');
    if (this.ebook.series && this.ebook.series.title && this.ebook.series.title.length > 256)
      addError('series', 'Series title too long');
    if (this.ebook.series_index && ! this.ebook.series_index.match(/^\d+$/))
      addError('series', 'Series index must be numeric');
    // Authors
    if (this.ebook.authors && this.ebook.authors.length > 20) addError('authors', 'Too many authors');
    // Genres
    if (this.ebook.genres && this.ebook.genres.length > 10) addError('genres', 'Too many genres');

    return errors.length === 0
  }

  cancel() {
    if (this.ebook.id) {
      this.router.navigateToRoute('ebook', {id:this.ebook.id});
    } else {
      this.router.navigate('welcome')
    }
  }

  get seriesLoader() {
    return start => this.client.getIndex('series', start);
  }
}
