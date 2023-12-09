import {BaseModel} from './base-model';

export class Bookshelf extends BaseModel {
  constructor(shelf) {
    super(shelf, ['name', 'description', 'public']);
  }

  validate(addError) {
    if (!this.name) addError('name', 'Name is mandatory!');
    if (this.name && this.name.length > 256) addError('name', 'Name too long');
    if (this.description && this.description.length > 10000) addError('description', 'Description too long');
  }
}
