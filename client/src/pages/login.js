import {Access} from 'lib/access';
import {inject, LogManager, bindable} from 'aurelia-framework';

let logger=LogManager.getLogger('login');

@inject(Access)
export class Login{
  title = 'Login';
  @bindable email='';
  @bindable password='';
  error=false;

    constructor(access){
        this.access = access;
    };

    login(){
        return this.access.login(this.email,this.password)
        .then( () => this.error = undefined)
        .catch(err=>{
            this.error={error:'Login Failed', errorDetail: (err.error? err.error: err)};
            logger.error("Login failure: "+err);
            //todo: get it from auth config?
            //this.router.navigate('login')
        });
    };

    canDeactivate() {
      return ! this.error;
    }


}
