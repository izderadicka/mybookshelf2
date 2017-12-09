
import {NotificationBase} from './notification-base';

export class NotificationMetadata extends NotificationBase{
    navigateTo() {
      this.router.navigateToRoute('conversions');
    }

    get progress() {
      return Math.round(100*this.notification.progress,2) || 0.00;
    }
}
