import {bindable,  inject, LogManager} from 'aurelia-framework';
import $ from 'jquery';

let logger = LogManager.getLogger('context-menu');

@inject(Element)
export class ContextMenu {
  @bindable items;
  @bindable header = 'Context Menu';
  @bindable width = 128;
  @bindable action;
  @bindable filter = ()=>true;
  @bindable isEnabled = ()=>true;

  constructor(elem) {
    this.elem = elem;
  }

  attached() {
    this.root = $('div.context-menu', this.elem);
    $(window).click((evt) => {
      if ($(evt.target).hasClass('disabled')) return;
      this.hide()});

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
    if (! this.isEnabled(item)) return false;
    if (this.action) this.action(item.value, this.context)
    else alert(`Selected ${item.value}`);
    this.hide();
  }

}
