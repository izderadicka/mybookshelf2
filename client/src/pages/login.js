import {Access} from 'lib/access';
import {inject, LogManager, bindable} from 'aurelia-framework';
import {Router} from 'aurelia-router';

let logger=LogManager.getLogger('login');

@inject(Access, Router)
export class Login{
  title = 'Login';
  @bindable email='';
  @bindable password='';
  error=false;

    constructor(access, router){
        this.access = access;
        this.router = router;
    };

    canActivate() {
    if (this.access.authenticated) return false;
    logger.debug('Login view canActivate');
    return this.access.refreshLogin().
    then(() => {
      if (this.access.authenticated) {
        this.router.navigateBack();
        return false;
      }
      else {
        return true;
      }
      })
    .catch(() => true);

    }

    login(){
        return this.access.login(this.email,this.password)
        .then( () => this.error = undefined)
        .catch(err=>{
            this.error={error:'Login Failed', errorDetail: (err.error? err.error: err)};
            logger.error("Login failure: "+err);
            this.password = '';
            //todo: get it from auth config?
            //this.router.navigate('login')
        });
    };

    canDeactivate() {
      return ! this.error;
    }


}
