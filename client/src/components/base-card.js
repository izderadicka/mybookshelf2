/*import {LogManager} from 'aurelia-framework';
const logger=LogManager.getLogger('base-card');
*/
export class BaseCard {

  delete(evt) {
    if (this.deleteAction) {
      this.deleteAction(evt)
      .then( () => {
      if (this.reloadAction) this.reloadAction(true);
    });
    }
  }

  edit(evt) {
    if (this.editAction) {
      this.editAction(evt)
      .then( (res) => {
        if (this.reloadAction && res !== 'noreload') this.reloadAction();
      })

    }
  }

}
