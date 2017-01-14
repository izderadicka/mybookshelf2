import {AuthService} from 'aurelia-auth';
import {Authentication} from 'aurelia-auth/authentication'
import {inject, LogManager} from 'aurelia-framework';
import {EventAggregator} from 'aurelia-event-aggregator';
import {Router} from 'aurelia-router';
import {HttpClient, json} from 'aurelia-fetch-client';

let logger=LogManager.getLogger('access');

const REFRESH_TOKEN = 'aurelia_refresh_token';

@inject(AuthService, Authentication, EventAggregator, Router, HttpClient)
export class Access {
  constructor(auth, authUtil, event, router, http) {
    this.auth=auth;
    this.util=authUtil;
    this.event=event;
    this.router = router;
    this.http = http;
    logger.debug(`AuthUtil ${authUtil}`);
  }

  get token() {
    return this.util.getToken()
  }

  get refreshToken() {
    let token = window.localStorage.getItem(REFRESH_TOKEN);
    if (token && this.isTokenValid(token)) return token;
  }

  isTokenValid(token) {
    let exp;
    try {
      let base64Url = token.split('.')[1];
      let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      exp = JSON.parse(window.atob(base64)).exp;
    } catch (error) {
      return false;
    }

    if (exp) {
      return Math.round(new Date().getTime() / 1000) <= exp;
    }

    }

  redirectToLogin() {
    this.util.setInitialUrl(window.location.href);
    var loginRoute = this.util.getLoginRoute();
    this.router.navigate(loginRoute);
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
    if (! token) return false;
    if (this.checkRoles(['superuser', 'admin'], token.roles)) return true
    else if (this.checkRoles(['user'], token.roles) && userId && userId == token.id ) return true;
    return false;
  }

  canDelete(userId) {
    //maybe later we can decide for more restrictive permission
    return this.canEdit(userId);
  }

  get authenticated() {
    return this.auth.isAuthenticated();
  }

  refreshLogin() {
    let refreshToken = this.refreshToken;
    if (! refreshToken) return Promise.reject(new Error('No valid refresh token available'));
    let token = this.token;
    if (! token) return Promise.reject(new Error('No previous token available'));
    let loginUrl = this.util.getLoginUrl();
    return this.http.fetch(loginUrl,
                    {method: 'POST',
                     headers: {"Authorization": `Bearer ${token}`},
                     body: json({refresh_token: refreshToken})})
              .then(resp => {
                if (resp.status != 200) throw new Error(`Http error status: ${resp.status}`) ;
                return resp.json();
              })
              .then(resp => {
                let newToken = resp.access_token
                if (newToken) {
                  this.auth.setToken(newToken);
                  this.event.publish('user-logged-in', {user:this.currentUser});
                } else {
                  throw new Error(`An Error in login refesh: ${resp.error}`);
                }
              })

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
        if (window.localStorage && response.refresh_token)
          window.localStorage.setItem(REFRESH_TOKEN, response.refresh_token)

        this.event.publish('user-logged-in', {user:this.currentUser});
      }
    });

  }

  logout() {
    window.localStorage.removeItem(REFRESH_TOKEN);
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
