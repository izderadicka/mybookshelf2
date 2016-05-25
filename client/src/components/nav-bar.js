import {bindable, inject, LogManager} from 'aurelia-framework'
import {Access} from 'lib/access';
import $ from 'jquery';

const logger=LogManager.getLogger('nav-bar');

@inject(Access)
export class NavBar {
  @bindable router;
  @bindable doSearch;

  constructor(access) {
    this.access=access;
  }

  get isAuthenticated() {
    return this.access.authenticated;
  }

  searchSubmitted(query) {
    logger.debug('navbar.compo'+ $('#skeleton-navigation-navbar-collapse'));
    $('#skeleton-navigation-navbar-collapse').collapse('hide');
    this.doSearch(query);

  }


}
