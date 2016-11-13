
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
    if (this.loader)
    this.loader.then (blob => {
      this.cover.src = URL.createObjectURL(blob);
      let holder = $('#cover-holder', this.elem);
      holder.empty().append(this.cover);
      })
    .catch(err => {
      logger.warn(`Cannot load cover: ${err}`);
    })
  }

  attached() {
    this.updateCover();
  }

  loaderChanged() {
    this.updateCover();
  }
}
