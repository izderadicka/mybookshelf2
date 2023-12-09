
import {bindable, inject} from 'aurelia-framework';
import $ from 'jquery'

@inject(Element)
export class Cover {
  @bindable loader

  constructor(elem) {
    this.elem =  elem;
    this.cover = new Image();
    this.cover.onload = function() {
        URL.revokeObjectURL(this.src);
      }
  }

  updateCover() {
    let holder = $('#cover-holder', this.elem);

    if (this.loader) {
    this.loader.then (result => {
      if (result instanceof Blob) {
        this.cover.src = URL.createObjectURL(result);
      } else {
        this.cover.src = result;
      }

      holder.empty().append(this.cover);
      })
    .catch(err => {
      logger.warn(`Cannot load cover: ${err}`);
    })
  } else {
    holder.empty();
  }
  }

  attached() {
    this.updateCover();
  }

  loaderChanged() {
    this.updateCover();
  }
}
