import {bindable, inject, LogManager, computedFrom} from 'aurelia-framework';
import $ from 'jquery';
import diacritic from 'diacritic'; // npm:diacritic package

let logger = LogManager.getLogger('autocomplete');

function startsWith(string, start) {
  string = diacritic.clean(string).toLowerCase();
  start = diacritic.clean(start).toLowerCase()
  return string.startsWith(start);
}

@inject(Element)
export class Autocomplete {
  @bindable value;
  @bindable search;
  @bindable loader = [];
  @bindable minLength = 1;

  @bindable valueKey = null;

  _suggestions = [];
  _selected = null;
  _prevSearch;
  _suggestionsShown = false;
  _ignoreChange = false;

  constructor(elem) {
    this.elem=elem;
  }

  searchChanged() {
    if (this._ignoreChange) {
      this._ignoreChange = false;
      return;
    }
    if (!this.search || this.search.length < this.minLength) {
      this._suggestions = [];
      this.hideSuggestions();
      return;
    }

    this.getSuggestions().then(suggestions => {
      this._suggestions = suggestions;
      if (this._suggestions.length) {
        this.showSuggestions();
      }

    });
  }

  attached() {
    this.suggestionsList = $('div.autocomplete-suggestion', this.elem)
    this.hideSuggestions()
  }

  getSuggestions() {
      logger.debug(`Get suggestions for ${this.search}`);
      if (Array.isArray(this.loader)) {
        return Promise.resolve(this.loader.filter(item => startsWith(item, this.search)));
      } else if (typeof this.loader === 'function'){
        return this.loader(this.search)
          .then(res => res.items);
      }
      return Promise.reject(new Error('Invalid loader'));
  }

  itemSelected(evt) {
    let selected = $(evt.target).attr('data-index');
    this.select(selected);
  }

  keyPressed(evt) {
    logger.debug(`Key pressed ${evt.keyCode}`);
    if (this._suggestionsShown) {
    let key = evt.keyCode;
    switch (key) {
      case 13: // Enter
      if (this._selected !== null) this.select(this._selected)
      break;
      case 40: // Down
      this._selected++;
      if (this._selected >= this._suggestions.length) this._selected = this._suggestions.length -1;
      this.makeVisible(this._selected);
      break;
      case  38: // Up
      this._selected--;
      if (this._selected < 0) this._selected = 0;
      this.makeVisible(this._selected);
      break;
    }
  }
    return true;
  }

  makeVisible(idx) {
    let item = $(`a[data-index="${idx}"]`, this.elem);
    this.suggestionsList.scrollTop(this.suggestionsList.scrollTop() + item.position().top);
  }

  select(idx) {
    let newValue = this.valueKey ? this._suggestions[idx][this.valueKey] : this._suggestions[idx];
    logger.debug(`Selected ${newValue}`);
    if (this.search !== newValue) this._ignoreChange = true;
    this.search = newValue;
    this.value = this._suggestions[idx];

    this.hideSuggestions()
  }

  hideSuggestions() {
    this._suggestionsShown = false;
    this._selected = null;
    this.suggestionsList.hide();
  }

  showSuggestions() {
    this._suggestionsShown = true;
    this._selected = this._suggestions.length ? 0 : null;
    this.suggestionsList.show();
  }


}
