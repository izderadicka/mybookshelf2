
import {NotificationBase} from './notification-base';

export class NotificationMetadata extends NotificationBase{
    navigateTo() {
      this.router.navigateToRoute('ebook', {id:this.notification.ebookId})
    }
}
