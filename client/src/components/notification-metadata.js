
import {bindable} from 'aurelia-framework'

export class NotificationMetadata {
    @bindable notification;

    get isReady() {
      return this.notification.status === 'success' && this.notification.result && ! this.notification.done;
    }
    navigate() {
      this.notification.done = true;
      window.location.href='#/upload-result/'+this.notification.result
    }
}
