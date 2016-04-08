import {bindable, inject, LogManager} from 'aurelia-framework'
import {AuthService} from 'aurelia-auth';
import $ from 'jquery';

const logger=LogManager.getLogger('nav-bar');

@inject(AuthService)
export class NavBar {
  @bindable router;
  @bindable doSearch;

  constructor(auth) {
    this.auth=auth;
  }

  get isAuthenticated() {
    return this.auth.isAuthenticated();
  }

  searchSubmitted(query) {
    logger.debug('navbar.compo'+ $('#skeleton-navigation-navbar-collapse'));
    $('#skeleton-navigation-navbar-collapse').collapse('hide');
    this.doSearch(query);

  }


}
