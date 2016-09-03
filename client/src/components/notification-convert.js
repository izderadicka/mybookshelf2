
import {NotificationBase} from './notification-base';

export class NotificationMetadata extends NotificationBase{
    navigate() {
      this.router.navigateToRoute('ebook', {id:this.notification.ebookId})
    }
}
