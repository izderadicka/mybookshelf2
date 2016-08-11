
import {bindable, inject} from 'aurelia-framework'
import {Router} from 'aurelia-router';

@inject(Router)
export class NotificationMetadata {
    @bindable notification;

    constructor(router) {
      this.router=router
    }

    get isReady() {
      return this.notification.status === 'success' && this.notification.result && ! this.notification.done;
    }
    navigate() {
      this.notification.done = true;
      this.router.navigateToRoute('upload-result', {id:this.notification.result})
    }
}
