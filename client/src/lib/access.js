import {AuthService} from 'aurelia-auth';
import {Authentication} from 'aurelia-auth/authentication'
import {inject, LogManager} from 'aurelia-framework';
import {EventAggregator} from 'aurelia-event-aggregator';

let logger=LogManager.getLogger('access')

@inject(AuthService, Authentication, EventAggregator)
export class Access {
  constructor(auth, authUtil, event) {
    this.auth=auth;
    this.util=authUtil;
    this.event=event;
    logger.debug(`AuthUtil ${authUtil}`);
  }

  get token() {
    return this.util.getToken()
  }

  hasRole(...requiredRoles) {
    let token = this.auth.getTokenPayload();
    if (! token) return false;
    let roles=this.auth.getTokenPayload().roles
    return requiredRoles.reduce((prev, curr) => prev || roles.includes(curr), false);
  }

  get currentUser() {
    if (this.auth.isAuthenticated()) {
      return this.auth.getTokenPayload().email;
    }
  }

  get authenticated() {
    return this.auth.isAuthenticated();
  }

  login(username, password) {
    return this.auth.login({username, password})
    .then(response=>{
      if (response.error) {
        this.error=true;
        throw new Error('Invalid login');
      } else {
        this.error=false;
        logger.debug("success logged: " + JSON.stringify(response));
        this.event.publish('user-logged-in', {user:this.currentUser});
      }
    })
    .catch(err=>{
        this.error=true;
        logger.error("Login failure: "+err);
        //todo: get it from auth config?
        window.location.href='#/login';
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
