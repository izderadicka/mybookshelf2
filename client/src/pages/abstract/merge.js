import {LogManager} from 'aurelia-framework';

let logger = LogManager.getLogger('merge');

export class Merge {
  constructor(client, router, access) {
    this.client = client;
    this.router = router;
    this.access = access;
    this.mergeTo = true;
  }

  canActivate(params) {
    if (! params.id) return false;
    return this.client.getOne(this.modelEntity, params.id)
    .then( b=> {
      this.entity=b;
      return this.canMerge();
      })
    .catch(err => {
      logger.error(`Entity fetch error: ${err}`);
      return false;
    })
  }

  canMerge() {
    return this.access.canDelete(this.entity.created_by);
  }

  get ready() {
    return this.entity.id && this.otherEntity && this.otherEntity.id;
  }

  cancel() {
    this.router.navigateToRoute(this.viewRoute, {id: this.entity.id});
  }

  merge() {
    this.error=null;
    if (this.entity && this.otherEntity) {
      let promise= this.mergeTo? this.client.merge(this.modelEntity, this.otherEntity.id, this.entity.id):
                                this.client.merge(this.modelEntity, this.entity.id, this.otherEntity.id);
      promise.then(res => {
        this.client.clearCache(this.modelEntity);
        this.router.navigateToRoute(this.viewRoute, {id: res.id});
      })
      .catch(err => {
        logger.error('Error in merge', err);
        this.error={error:'Server Error', errorDetail:err};
      });
  }
}

  get fullMerge() {
    return this.access.hasRole('superuser')
  }


  get filterOutThisEntity() {
    return b => b.id !== this.entity.id;
  }

  get loader() {
    return start => this.client.getIndex(this.modelEntity, start);
  }

}
