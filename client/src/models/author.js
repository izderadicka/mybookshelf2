import {BaseModel} from './base-model';

export class Author extends BaseModel {
  constructor(author) {
    super(author, ['first_name', 'last_name']);
  }

  validate(addError) {
    if (!this.last_name) addError('last_name', 'Last name is mandatory!');
    if (this.last_name && this.last_name.length > 256) addError('last_name', 'Last name too long');
    if (this.first_name && this.first_name.length > 256) addError('first_name', 'First name too long');
  }
}
