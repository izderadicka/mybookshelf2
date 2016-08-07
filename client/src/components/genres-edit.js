import {LogManager, inject, computedFrom, bindable, bindingMode} from 'aurelia-framework';

export class GenresEdit {
  @bindable allGenres;
  @bindable genres;
  _selected;

  hasId(id) {
    if (!this.genres) return false;
    for (var genre of this.genres) {
      if (id === genre.id) return true
    }
    return false;
  }

  get visibleGenres() {
    return this.allGenres.filter(item => ! this.hasId(item.id));
  }

  addGenre() {
    if (! this.genres) this.genres = [];
    if (this._selected) this.genres.push(this._selected);
    this._selected = undefined;
  }

  removeGenre(selected) {
    if (selected !== undefined) this.genres.splice(selected,1);
  }
}
