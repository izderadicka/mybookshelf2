import {LogManager, inject, computedFrom, bindable, bindingMode} from 'aurelia-framework';
import {ApiClient} from 'lib/api-client';
import $ from 'jquery';
import 'select2';
import {dispatchCustomEvent} from 'lib/utils';

let logger = LogManager.getLogger('genres-select');

@inject(Element, ApiClient)
export class GenresSelect {
  @bindable({defaultBindingMode: bindingMode.twoWay}) genres;
  @bindable placeholder;

  constructor(element,client) {
    this.element = element;
    this.client =  client;
  }

  created() {
    this.client.getManyUnpagedCached('genres')
    .then(data => {
      this.options = data.map(i => { return {value: i.id, label:i.name}})
    })
    .catch(err=> logger.error(`Cannot fetch genres ${err}`))
  }

  attached() {
    $(this.element).find('select')
            .select2({
              placeholder: this.placeholder
            })
            .on('change', (event) => {
                let changeEvent;
                let genres = $(event.target).val();
                this.genres = genres;
                dispatchCustomEvent('selected', this.element,
                                    {
                                      value: genres
                                  });

            });
  }

  isSelected(option) {
    return this.genres && this.genres.find(i => i == option.value);
  }

}
