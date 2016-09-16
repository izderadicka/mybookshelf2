import {Access} from 'lib/access';

describe('When using Access class', () => {
  var auth = {getTokenPayload() {},
              isAuthenticated() {return true}},
      authUtil = {},
      event = {},
      router = {},
      access;

  beforeEach(() => {
      access = new Access(auth, authUtil, event, router)
    });

   it('there is no role if not in token', ()=>{
     spyOn(auth, 'getTokenPayload').and.returnValue({});
     expect(access.hasRole('user')).toBeFalsy();
   });

   it('should recognize roles provided', ()=>{
     spyOn(auth, 'getTokenPayload').and.returnValue({roles:['user', 'admin']});
     expect(access.hasRole('user')).toBeTruthy();
     expect(access.hasRole('admin')).toBeTruthy();
     expect(access.hasRole('uknown')).toBeFalsy();
     expect(auth.getTokenPayload).toHaveBeenCalledTimes(3);
   });

   it('should provide user name', () => {
     spyOn(auth, 'getTokenPayload').and.returnValue({user_name:'user', email:'email'});
     expect(access.currentUser).toEqual('email');
   });

   it('superuser can edit everything', () => {
     spyOn(auth, 'getTokenPayload').and.returnValue({roles:['user', 'superuser', 'admin'], id:99});
     expect(access.canEdit(33)).toBeTruthy();
   });

   it('admin can edit everything', () => {
     spyOn(auth, 'getTokenPayload').and.returnValue({roles:['user',  'admin'], id:99});
     expect(access.checkRoles(['superuser', 'admin'],['user', 'admin'])).toBeTruthy();
     expect(access.canEdit(33)).toBeTruthy();
   });

   it('user only his objects', () => {
     spyOn(auth, 'getTokenPayload').and.returnValue({roles:['user'], id:99});
     expect(access.canEdit(99)).toBeTruthy();
     expect(access.canEdit(33)).toBeFalsy();
   });



});
