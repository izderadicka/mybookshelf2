
import {NotificationBase} from './notification-base';

export class NotificationMetadata extends NotificationBase{
    navigate() {
      this.router.navigateToRoute('conversions');
    }

    get progress() {
      return Math.round(100*this.notification.progress,2) || 0.00;
    }
}
