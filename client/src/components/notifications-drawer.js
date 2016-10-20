import {Notification} from 'lib/notification';
import {inject, LogManager} from 'aurelia-framework';
import {Configure} from  'lib/config/index';
import $ from 'jquery';

let logger = LogManager.getLogger('notifications-drawer');

@inject(Element, Notification, Configure)
export class NotificationsDrawer {

  constructor(elem,notif, config) {
      this.notif=notif;
      this.elem = elem;
      this.attention;
      this.attentionTimeout = (config.get('notificationAttentionTimeout') || 20) * 1000;
      this._dispose = notif.addObserver(this.onNotificationsUpdated.bind(this));

  }

  attached() {
    this.root = $('#drawer-notifications', this.elem);
    this.icon = $('#drawer-icon', this.elem);
  }

  onNotificationsUpdated(action, status) {
    logger.debug(`Got update ${action} ${status}`);
    if (action === 'update' && (status === 'success' || status === 'error'))
      this.attention = true;
      this._to = window.setTimeout(() => {
        window.clearTimeout(this._to);
        this.attention = false;
      },
        this.attentionTimeout);
  }

  get fold() {
    return ! this.root.hasClass('open')

  }

  drawerMove() {
    this.attention = false;
    return true;
  }

hide() {
  this.root.drawer('hide');
}

clearFinished() {
  this.notif.clearFinished();
  if (this.notif.empty) this.hide();
}
}
