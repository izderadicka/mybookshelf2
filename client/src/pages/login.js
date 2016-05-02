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

        return this.auth.login({username:this.email, password:this.password})
        .then(response=>{
          if (response.error) {
            this.error=true;
            throw new Error('Invalid login');
          } else {
            this.error=false;
            logger.debug("success logged: " + JSON.stringify(response));
          }
        })
        .catch(err=>{
            this.error=true;
            logger.error("login failure: "+err);
            //todo: get it from auth config?
            window.location.href='#/login';
        });
    };

    authenticate(name){
        return this.auth.authenticate(name, false, null)
        .then((response)=>{
            logger.debug("auth response " + JSON.stringify(response));
        });
    }
}
