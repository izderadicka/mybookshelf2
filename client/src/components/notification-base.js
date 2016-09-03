
import {bindable, inject} from 'aurelia-framework'
import {Router} from 'aurelia-router';

@inject(Router)
export class NotificationBase {

    constructor(router) {
      this.router=router
    }

    get isReady() {
      return this.notification.status === 'success' && this.notification.result && ! this.notification.done;
    }

    activate(model) {
      this.notification = model;
    }

    navigate() {
      throw new Error('Not Implemented');
    }
}
