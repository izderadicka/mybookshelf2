import {bindable, bindingMode, LogManager} from 'aurelia-framework';

let logger = LogManager.getLogger('rating')

export class Rating {
  @bindable numStars=5;
  @bindable({defaultBindingMode: bindingMode.twoWay}) rating;
  @bindable size = 1.0;
  @bindable max = 100;
  @bindable onRatingChange;
  @bindable readOnly;


  constructor() {
  }

  bind() {
    this.stars=[];
    for (let i=0; i<this.numStars; i++) this.stars.push({rated:false, proposed:false});
    logger.debug('Bound rating '+this.rating);
    this.updateRating(this.rating);
  }

  updateRating(v) {
    let idx = Math.round(v/(this.max / this.numStars)) - 1
    for (let i=0; i<=idx; i++) this.stars[i].rated=true;
    for (let i=idx+1; i < this.numStars; i++) this.stars[i].rated=false;
  }

  ratingChanged(v) {
    logger.debug('Rating changed '+this.rating);
    this.updateRating(v)
    if (this.onRatingChange) {
      let res = this.onRatingChange(this.rating);
      if (res instanceof Promise) {
        res.catch(err => logger.error('Rating update failed: '+ err));
      }
    }

  }

  propose(idx) {
    if (this.readOnly) return;
    for (let i=0; i<=idx; i++) this.stars[i].proposed=true;
    for (let i=idx+1; i < this.numStars; i++) this.stars[i].proposed=false;
  }

  clearProposed() {
    if (this.readOnly) return;
    for (let i=0; i<this.numStars; i++) this.stars[i].proposed=false;
  }

  rate(idx) {
    if (this.readOnly) return;
    this.rating = this.max / this.numStars * (idx+1);
    this.clearProposed()

  }

  resetRating() {
    this.rating = null;
  }

}
