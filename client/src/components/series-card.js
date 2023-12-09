import {inject, bindable, LogManager} from 'aurelia-framework';
import {BaseCard} from './base-card';

const logger=LogManager.getLogger('series-card');

export class SeriesCard extends BaseCard{
  @bindable series;
  @bindable description;
  @bindable editAction;
  @bindable deleteAction;
  @bindable reloadAction;

}
