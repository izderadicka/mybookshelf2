import {LogManager, inject, computedFrom, bindable, bindingMode} from 'aurelia-framework';

export class ErrorAlert {
  @bindable({
    defaultBindingMode: bindingMode.twoWay
  }) error;

  clearError() {
    this.error=undefined;
  }
}
