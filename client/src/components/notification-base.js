
import {bindable, inject} from 'aurelia-framework'
import {Router} from 'aurelia-router';
import {NotificationsDrawer} from 'components/notifications-drawer';

@inject(Router, NotificationsDrawer)
export class NotificationBase {

    constructor(router, drawer) {
      this.router = router;
      this.drawer = drawer;
    }

    get isReady() {
      return this.notification.status === 'success' && this.notification.result && ! this.notification.done;
    }

    activate(model) {
      this.notification = model;
    }

    navigateTo() {
      throw new Error('Not Implemented');
    }

    navigate() {
      this.drawer.hide();
      this.navigateTo();
    }
}
