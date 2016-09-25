import {LogManager, inject, computedFrom, bindable, bindingMode} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import $ from 'jquery';

let logger = LogManager.getLogger('authors-edit');

@inject(ApiClient)
export class AuthorsEdit {
  @bindable authors;
  _author;
  _authorSelected;

  constructor(client) {
    this.client=client;
  }

  get loaderAuthors() {
    return start => this.client.getIndex('authors', start);
  }

  getFullName(item) {
    let name= item.first_name ? item.last_name + ', ' + item.first_name : item.last_name
    //if (!item.id) name+= ' (new)';
    return name
  }

  //@computedFrom('authors')
  get authorsVisible() {
    if (this.authors && this.authors.length) {
      return this.authors.map(this.getFullName)
    }
  }


  _addIfNotExists(author) {
    for (var item of this.authors) {
      if (item.last_name === author.last_name && item.first_name === author.first_name) return;
    }
    this.authors.push(author);
    }

  addAuthor() {
    if (! this.authors) this.authors = [];
    if (this._authorSelected) {
      this._addIfNotExists(this._authorSelected);
      this._author = '';
    } else if (this._author) {
      this._addIfNotExists(this.splitFullName(this._author));
      this._author = '';
    }
  }

  onSelect(evt) {
    let {displayValue, selectedValue} = evt.detail;
    if (selectedValue) {
      this._addIfNotExists(selectedValue);
    } else if (displayValue) {
      this._addIfNotExists(this.splitFullName(displayValue));
    }
  }

  removeAuthor(selected) {
    if (selected !== undefined) this.authors.splice(selected,1);

  }

  splitFullName(name) {
    let parts = name.split(',').map(x => x.trim());
    let splittedName = {last_name: parts[0]}
    if (parts.length > 1) splittedName.first_name = parts.slice(1).join(' ');
    return splittedName;
  }
}
