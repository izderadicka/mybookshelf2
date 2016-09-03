
import {NotificationBase} from './notification-base';

export class NotificationMetadata extends NotificationBase {

    navigate() {
      this.notification.done = true;
      this.router.navigateToRoute('upload-result', {id:this.notification.result})
    }
}
