
import {NotificationBase} from './notification-base';

export class NotificationCover extends NotificationBase{
    navigateTo() {
      this.router.navigateToRoute('ebook', {id:this.notification.ebookId})
    }
}
