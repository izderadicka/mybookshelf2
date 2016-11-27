import {inject, bindable, LogManager} from 'aurelia-framework';

const logger=LogManager.getLogger('series-card');

export class SeriesCard {
  @bindable series;
  @bindable description;
  @bindable editAction;
  @bindable deleteAction;
  @bindable reloadAction;


  delete(evt) {
    if (this.deleteAction) {
      this.deleteAction(evt)
      .then( () => {
      if (this.reloadAction) this.reloadAction();
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
