import {bindable, bindingMode} from 'aurelia-framework';

export class MergeDirection {
  @bindable name
  @bindable readOnly;
  @bindable({
    defaultBindingMode: bindingMode.twoWay
  }) mergeTo;
}
