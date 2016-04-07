import {bindable, inject} from 'aurelia-framework'
import {AuthService} from 'aurelia-auth';

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

  
}
