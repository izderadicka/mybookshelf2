import {bindable, inject, LogManager} from 'aurelia-framework'
import {Access} from 'lib/access';
import {WSClient} from 'lib/ws-client';
import $ from 'jquery';

const logger=LogManager.getLogger('nav-bar');

@inject(Access, WSClient)
export class NavBar {
  @bindable router;
  @bindable doSearch;

  constructor(access, wsClient) {
    this.access=access;
    this.wsClient=wsClient;
  }

  get isConnected() {
    return this.wsClient.isConnected;
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
