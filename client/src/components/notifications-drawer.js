import {Notification} from 'lib/notification';
import {inject, LogManager} from 'aurelia-framework';

@inject(Notification)
export class NotificationsDrawer {

  constructor(notif) {
      this.notif=notif;
  }

}
