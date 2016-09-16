import {AuthService} from 'aurelia-auth';
import {Authentication} from 'aurelia-auth/authentication'
import {inject, LogManager} from 'aurelia-framework';
import {EventAggregator} from 'aurelia-event-aggregator';
import {Router} from 'aurelia-router';

let logger=LogManager.getLogger('access')

@inject(AuthService, Authentication, EventAggregator, Router)
export class Access {
  constructor(auth, authUtil, event, router) {
    this.auth=auth;
    this.util=authUtil;
    this.event=event;
    this.router = router;
    logger.debug(`AuthUtil ${authUtil}`);
  }

  get token() {
    return this.util.getToken()
  }

  hasRole(...requiredRoles) {
    let token = this.auth.getTokenPayload();
    if (! token) return false;
    let roles=token.roles
    if (! roles) return false;
    return this.checkRoles(requiredRoles, roles);
  }

  checkRoles(requiredRoles, roles) {
    return requiredRoles.reduce((prev, curr) => prev || roles.includes(curr), false);
  }

  get currentUser() {
    if (this.auth.isAuthenticated()) {
      return this.auth.getTokenPayload().email;
    }
  }

  canEdit(userId) {
    let token = this.auth.getTokenPayload();
    if (this.checkRoles(['superuser', 'admin'], token.roles)) return true
    else if (this.checkRoles(['user'], token.roles) && userId && userId == token.id ) return true;
    return false;
  }

  get authenticated() {
    return this.auth.isAuthenticated();
  }

  login(username, password) {
    return this.auth.login({username, password})
    .then(response=>{
      if (response.error) {
        let err=new Error('Invalid login');
        err.error=response.error;
        throw err;
      } else {
        logger.debug("success user logged in: " + JSON.stringify(response));
        this.event.publish('user-logged-in', {user:this.currentUser});
      }
    });

  }

  logout() {
    this.auth.logout();
    this.event.publish('user-logged-out');

  }

  signalState() {
    if (this.authenticated) {
      this.event.publish('user-logged-in', {user:this.currentUser});
    } else {
      this.event.publish('user-logged-out');
    }
  }

  authenticate(name){
      return this.auth.authenticate(name, false, null)
      .then((response)=>{
          logger.debug("auth response " + JSON.stringify(response));
      });
  }

}
