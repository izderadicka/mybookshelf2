import {BaseModel} from './base-model';

export class Series extends BaseModel {
  constructor(series) {
    super(series, ['title']);
  }

  validate(addError) {
    if (!this.title) addError('title', 'Title is mandatory!');
    if (this.title && this.title.length > 256) addError('title', 'Title too long');
  }
}
