import {BaseModel} from './base-model';

export class BookshelfItem extends BaseModel {
  constructor(shelf) {
    super(shelf, ['name', 'description', 'order', 'ebook.id', 'series.id']);
  }

  validate(addError) {
    if (this.name && this.name.length > 256) addError('name', 'Name too long');
    if (this.note && this.note.length > 10000) addError('description', 'Description too long');
    if (this.order && ! Number.isInteger(this.order)) addError('order', 'Order must be integer');
    if (! this.ebook.id && ! this.series.id) addError('item', 'Either ebook or series must be here');
    if (this.ebook.id &&  this.series.id) addError('item', 'Cannot have both ebook and series');
  }
}
