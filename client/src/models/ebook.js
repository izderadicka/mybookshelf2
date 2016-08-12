import {BindingEngine, inject, LogManager} from 'aurelia-framework';
import {Container} from 'aurelia-dependency-injection';

let logger = LogManager.getLogger('ebook');

export class Ebook {

  _editableProps=['title', 'authors[]', 'genres[]', 'language.id', 'series', 'series_index'];

  constructor(ebook) {
    let bindingEngine = Container.instance.get(BindingEngine);
    if (ebook) Object.assign(this, ebook);

    this._disposers=[];
    this._changed = new Set();

    let bind = (prop, asArray) => {
      let observer;
      let obj = this;
      let parts=prop.split('.');
      let propName=parts[0];

      while (parts.length >1) {
        let disp =  bindingEngine.propertyObserver(obj, parts[0])
          .subscribe((n,o) => this.changed(propName));
        this._disposers.push(disp);
        let newObj = obj[parts[0]];
        if (!newObj) {
          newObj = {};
          obj[parts[0]] = newObj;
        }
        obj = newObj;
        prop = parts[1];
        parts.shift();
      }

      if (asArray) {
        if (!obj[prop]) obj[prop] = [];
        observer = bindingEngine.collectionObserver(obj[prop]);
      } else {
        observer=bindingEngine.propertyObserver(obj, prop);
      }
      let disp = observer.subscribe((n,o) => this.changed(propName,n,o));
      this._disposers.push(disp);
    }

    for (let [prop, asArray] of this.editableProps2)
      bind(prop, asArray);
  }

  get editableProps() {
    return this._editableProps.map(p => {
      return p.endsWith('[]')? p.slice(0,-2):p;
    })
  }

  get editableProps2() {
    return this._editableProps.map(p => {
      return p.endsWith('[]')? [p.slice(0,-2), true]:[p, false];
    })
  }

  isNew() {
    return ! this.id ;
  }

  changed(prop, n, o) {
    logger.debug('Property changed '+prop);
    this._changed.add(prop);
  }

  dispose() {
    this._disposers.forEach(d => d());
  }

  validate(addError) {
    // Title
    if (!this.title) addError('title', 'Title is mandatory!');
    if (this.title && this.title.length > 256) addError('title', 'Title too long');
    // Language
    if ( !this.language || !this.language.id) addError('language', 'Language is mandatory');
    // Series
    if ( this.series && this.series.title && ! this.series_index)
      addError('series', 'If series title is present then series index is mandatory');
    if ( !(this.series && this.series.title) &&  this.series_index)
      addError('series', 'If series index is present then series title is mandatory');
    if (this.series && this.series.title && this.series.title.length > 256)
      addError('series', 'Series title too long');
    if (this.series_index && ! this.series_index.match(/^\d+$/))
      addError('series', 'Series index must be numeric');
    // Authors
    if (this.authors && this.authors.length > 20) addError('authors', 'Too many authors');
    // Genres
    if (this.genres && this.genres.length > 10) addError('genres', 'Too many genres');

  }

  prepareData() {
    let data = {}

    let shrink = function(obj) {
      if  (!obj) return null;
      if (obj.hasOwnProperty('id') && obj.id) {
        return {id:obj.id}
      } else {
        let newObj = {}
        for (let prop of Object.keys(obj)) {
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

    for (let prop of this.editableProps) {
      if (this.isNew() || this._changed.has(prop)) {
        let val = this[prop];
        if (Array.isArray(val))
          val = shrinkList(val);
        else if (typeof val === 'object')
          val = shrink(val)
        data[prop] = val;
      }
    }
    /*
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

    */

    if (! this.isNew() && Object.keys(data).length) {
      data.id = this.id;
      data.version_id = this.version_id;
    }

    logger.debug(`New data : ${JSON.stringify(data)}`);
    return data;

  }

}
