import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';

const logger = LogManager.getLogger('add-to-shelf-button');

@inject(Router, ApiClient)
export class AddToShelfButton {
  @bindable what;
  @bindable item;
  constructor(router, client) {
    this.client = client;
    this.router = router;
    this.shelves = [];
  }

  showAddToShelf() {
    this.router.navigateToRoute('add-to-shelf', {what:this.what, id:this.item.id})
  }

  created() {
    this.client.getMany('bookshelves/mine', 1, 5, '-modified')
    .then( res => {
      this.shelves = res.data;
    })
    .catch( err => logger.error('Error when loading shelves', err))
  }

  addTo(shelf) {
    let postObj = this.what == 'ebook'? {ebook:{id:this.item.id}}:{series: {id:this.item.id}};
    this.client.post(`bookshelves/${shelf.id}/add`, postObj)
    .then( () => {
      logger.debug('Added to shelf')
    })
    .catch((err) => {
      logger.error('Error posting data to server', err);
      alert('Add to shelf failed');
    })
  }
}
