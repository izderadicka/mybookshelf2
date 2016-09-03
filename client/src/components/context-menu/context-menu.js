import {bindable,  inject, LogManager} from 'aurelia-framework';
import $ from 'jquery';

let logger = LogManager.getLogger('context-menu');

inject(Element)
export class ContextMenu {
  @bindable items;
  @bindable title = 'Context Menu';
  @bindable width = 128;
  @bindable action;

  constructor(elem) {
    this.elem = elem
  }

  attached() {
    this.root = $('div.context-menu', this.elem);
    $(window).click(() => this.hide());

  }

  show(evt, context) {
    this.context = context;
    evt.stopPropagation();
    this.root.show();
    let {pageX,pageY} = evt;
    this.root.offset({top:pageY, left:pageX});

    let {top,left} = this.root.offset()
    let win = $(window);
    let bottom = top+this.root.height();
    let right = left + this.root.width();

    if (right > win.width()) pageX = pageX - this.root.width();
    if (bottom > win.height()) pageY = pageY - this.root.height();
    this.root.offset({top:pageY, left:pageX});

  }

  hide() {
    this.root.hide();
  }

  select(item) {
    if (this.action) this.action(item.value, this.context)
    else alert(`Selected ${item.value}`);
    this.hide();
  }

}
