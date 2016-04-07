import {AuthService} from 'aurelia-auth';
import {inject, LogManager} from 'aurelia-framework';
const logger=LogManager.getLogger('login')

@inject(AuthService)
export class Login{
  title = 'Login';
  email='';
  password='';
  error=false;

    constructor(auth){
        this.auth = auth;
    };

    login(){

        return this.auth.login(this.email, this.password)
        .then(response=>{
            this.error=false;
            logger.debug("success logged: " + JSON.stringify(response));
        })
        .catch(err=>{
            this.error=true;
            logger.error("login failure: "+err);
        });
    };

    authenticate(name){
        return this.auth.authenticate(name, false, null)
        .then((response)=>{
            logger.debug("auth response " + JSON.stringify(response));
        });
    }
}
