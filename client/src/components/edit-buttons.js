import {containerless} from 'aurelia-framework';

@containerless
export class EditButtons {

  bind(bindingContext, overrideContext) {
    this.p = bindingContext;
  }
}
