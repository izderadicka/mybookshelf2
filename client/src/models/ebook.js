import {BindingEngine, inject, LogManager} from 'aurelia-framework';
import {Container} from 'aurelia-dependency-injection';
import {BaseModel} from './base-model';

let logger = LogManager.getLogger('ebook');


export class Ebook extends BaseModel{

  constructor(ebook) {
    super(ebook,
    ['title', 'authors[]', 'genres[]', 'language.id', 'series', 'series_index']);

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
    if (this.series_index && ! Number.isInteger(this.series_index) && ! this.series_index.match(/^\d+$/))
      addError('series', 'Series index must be numeric');
    // Authors
    if (this.authors && this.authors.length > 20) addError('authors', 'Too many authors');
    // Genres
    if (this.genres && this.genres.length > 10) addError('genres', 'Too many genres');

  }

}
