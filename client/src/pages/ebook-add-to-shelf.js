import {LogManager, inject, bindable} from 'aurelia-framework';
import {Router} from 'aurelia-router';
import {ApiClient} from 'lib/api-client';

const logger = LogManager.getLogger('ebook-add-to-shelf');

@inject(Router, ApiClient)
export class EbookAddToShelf {
  constructor(router, client) {
    this.client = client;
    this.router = router;
  }

  activate({what, id}, route) {
    return this.client.getOne(what,id)
    .then ( (item) =>{
      this.item = item;
      this.what = what;
      route.navModel.setTitle(`Add "${item.title}" to Bookshelf`);
    })
    .catch((err) => {
      this.error={error:'Fetch Error', errorDetail: err};
      logger.error('Server error loading item', err);
    })
  }

  get ready() {
    return this.shelf && this.shelf.length >= 3;
  }

  get loaderShelves() {
    return start => this.client.getIndex('bookshelves/mine', start);
  }

  goToItemPage() {
    this.router.navigateToRoute(this.what == 'ebooks'?'ebook':'series', {id:this.item.id})
  }

  cancel() {
    this.goToItemPage()
  }

  add() {
    let shelfLoader;
    if (this.existingShelf) {
      shelfLoader = Promise.resolve({id:this.existingShelf.id});
    } else {
      shelfLoader = this.client.post(`bookshelves`, {name: this.shelf})

    }
    shelfLoader.then ( ({id}) => {
      let postObj = this.what == 'ebooks'? {ebook_id:this.item.id}:{series_id:this.item.id};
      this.client.post(`bookshelves/${id}/add`, postObj)
      .then( () => {
        this.goToItemPage();
      })
      .catch((err) => {
        this.error = {error:'Post error', errorDetail:err};
        logger.error('Error posting data to server', err);
      })
    })
  }

}
