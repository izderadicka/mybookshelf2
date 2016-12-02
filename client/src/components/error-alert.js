import {LogManager, inject, computedFrom, bindable, bindingMode} from 'aurelia-framework';

export class ErrorAlert {
  @bindable({
    defaultBindingMode: bindingMode.twoWay
  }) error;

  @bindable dismissible = true;

  clearError() {
    this.error=undefined;
  }

  @computedFrom('error.errorDetail')
  get detail() {
    return JSON.stringify(this.error.errorDetail);
  }
}
