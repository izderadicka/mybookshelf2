import {AuthService, BaseConfig} from 'aurelia-auth';
import {Authentication} from 'aurelia-auth/authentication'
import {inject, LogManager} from 'aurelia-framework';

let logger=LogManager.getLogger('access')

@inject(AuthService, Authentication)
export class Access {
  constructor(auth, authUtil) {
    this.auth=auth;
    this.util=authUtil;
    logger.debug(`AuthUtil ${authUtil}`);
  }

  get token() {
    return this.util.getToken()
  }

  has_role(...requiredRoles) {
    let roles=this.auth.getTokenPayload().roles
    return requiredRoles.reduce((prev, curr) => prev || roles.includes(curr), false);
  }

}
