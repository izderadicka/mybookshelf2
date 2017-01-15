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
    if (this.error) {
    if (this.error.errorDetail instanceof Error)
      return `${this.error.errorDetail.name}: ${this.error.errorDetail.message}`
    else
      return JSON.stringify(this.error.errorDetail);
  }}
}
