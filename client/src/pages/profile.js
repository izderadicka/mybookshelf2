import {inject} from 'aurelia-framework';
import {Access} from 'lib/access';

@inject(Access)
export class Profile {

  constructor(access) {
    this.access = access;
  }

  activate() {
    this.user = this.access.currentUserInfo
  }

}
