
import {NotificationBase} from './notification-base';

export class NotificationCover extends NotificationBase{
    navigate() {
      this.router.navigateToRoute('ebook', {id:this.notification.ebookId})
    }
}
