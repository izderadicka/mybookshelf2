import {bindable, bindingMode, inject, LogManager, computedFrom} from 'aurelia-framework';
import $ from 'jquery';
import diacritic from 'diacritic'; // npm:diacritic package

let logger = LogManager.getLogger('autocomplete');

const CACHE_DURATION = 60000; //ms

function startsWith(string, start) {
  string = diacritic.clean(string).toLowerCase();
  start = diacritic.clean(start).toLowerCase()
  return string.startsWith(start);
}

@inject(Element)
export class Autocomplete {
  @bindable({
    defaultBindingMode: bindingMode.twoWay
  }) value; // value of input
  @bindable({
    defaultBindingMode: bindingMode.twoWay
  }) selectedValue; // this will be selected value from suggestions - full value
  @bindable loader = []; // can be either array of suggestions or function returning Promise resolving to such array
  @bindable minLength = 1; // min length of input to start search and suggest
  @bindable valueKey = null; // name of value property, null means use use whole suggestion
  @bindable suggestionTemplate = null; // template to display a suggestion - if none string value of suggestion is shown
  @bindable additionalClass; // additional classes for input control
  @bindable placeholder = ''; // placeholder for input control
  @bindable resetAfterSelect = false; // after value is selected and event is fired reset value to empty string;

  _suggestions = [];
  _selected = null;
  _suggestionsShown = false;
  _ignoreChange = false;
  _cache;
  _attached = false;

  constructor(elem) {
    this.elem = elem;
  }

  valueChanged() {
    if (!this._attached) return;

    if (this._ignoreChange) {
      this._ignoreChange = false;
      return;
    }
    this.selectedValue = undefined;
    if (!this.value || this.value.length < this.minLength) {
      this._suggestions = [];
      this.hideSuggestions();
      return;
    }

    this.getSuggestions(this.value).then(suggestions => {
      this._suggestions = suggestions;
      if (this._suggestions.length) {
        this.showSuggestions();
      } else {
        this.hideSuggestions();
      }

    });
  }

  attached() {
    this.suggestionsList = $('div.autocomplete-suggestion', this.elem)
    this._attached = true;
    this.hideSuggestions()
  }

  getSuggestionValue(item) {
    if (!this.valueKey) {
      return item;
    } else if (typeof this.valueKey === 'string') {
      return item[this.valueKey];
    } else if (typeof this.valueKey === 'function') {
      return this.valueKey(item)
    }
  }

  getSuggestions(forValue) {
    logger.debug(`Get suggestions for ${forValue}`);
    if (Array.isArray(this.loader)) {
      return Promise.resolve(this.loader.filter(item =>
        startsWith(this.getSuggestionValue(item), forValue)));
    } else if (typeof this.loader === 'function') {
      if (this._cache && startsWith(forValue, this._cache.search) &&
        new Date() - this._cache.ts <= CACHE_DURATION) {
        return Promise.resolve(this._cache.items.filter(
          item => startsWith(this.getSuggestionValue(item), forValue)
        ))
      }
      return this.loader(forValue)
        .then(res => {

          if (res.items.length === res.total) {
            // we have all results, can cache
            this._cache = {
              search: forValue,
              items: res.items,
              ts: new Date()
            }
          }

          // if inputed value already changed do not return these suggestions
          if (this.value !== forValue) return [];

          return res.items;
        });
    }
    return Promise.reject(new Error('Invalid loader'));
  }


  keyPressed(evt) {
    let key = evt.keyCode;
    //logger.debug(`Key pressed ${key}`);
    if (this._suggestionsShown) {
      switch (key) {
        case 13: // Enter
          if (this._selected !== null) this.select(this._selected)
          break;
        case 40: // Down
          this._selected++;
          if (this._selected >= this._suggestions.length) this._selected = this._suggestions.length - 1;
          this.makeVisible(this._selected);
          break;
        case 38: // Up
          this._selected--;
          if (this._selected < 0) this._selected = 0;
          this.makeVisible(this._selected);
          break;
        case 27: // Escape
          this.hideSuggestions();
          break;
        }
      } else {
        if (key === 13 && this.value)
          this.fireSelectedEvent(this.value, this.selectedValue);
      }

    return true;
  }

  fireSelectedEvent(value, selectedValue) {
    let selectEvent;

    if (window.CustomEvent) {
        selectEvent = new CustomEvent('selected', {
            detail: {displayValue:value, selectedValue},
            bubbles: true
        });
    } else {
        selectEvent = document.createEvent('CustomEvent');
        selectEvent.initCustomEvent('select', true, true, {
            detail: {displayValue:value, selectedValue}

        });
    }
    this.elem.dispatchEvent(selectEvent);
    if (this.resetAfterSelect) {
      this._ignoreChange = false;
      this.value="";
    }
  }

  makeVisible(idx) {
    let item = $(`a[data-index="${idx}"]`, this.elem);
    if (item && item.position()) {
      this.suggestionsList.scrollTop(this.suggestionsList.scrollTop() + item.position().top);
    }
  }

  select(idx) {
    logger.debug(`Selected index ${idx}`);
    let newValue = this.getSuggestionValue(this._suggestions[idx]);
    logger.debug(`Selected ${newValue}`);
    if (this.value !== newValue) this._ignoreChange = true;
    this.value = newValue;
    this.selectedValue = this._suggestions[idx];
    this.hideSuggestions();
    this._suggestions = [this.selectedValue];
    if (this.selectedValue) {
      this.fireSelectedEvent(this.value, this.selectedValue)
    }
  }

  hideSuggestions() {
    this._suggestionsShown = false;
    this._selected = null;
    this.suggestionsList.hide();
  }

  showSuggestions() {
    if (this._suggestions) {
    this._suggestionsShown = true;
    this._selected = this._suggestions.length ? 0 : null;
    this.suggestionsList.show();
    this.makeVisible(this._selected);
  }
  }


}
