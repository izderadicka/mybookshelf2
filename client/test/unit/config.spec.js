import {Configure} from 'lib/config/index';
import {DefaultLoader} from 'aurelia-loader-default';


describe('When using Configure', () => {

let loader = new DefaultLoader();
var conf = null;

beforeEach(() => {
  conf = new Configure();
})
it('it should contain default instance properties', () => {
expect(conf._config).toBeDefined();
});

it('it should load config with values', () =>{

    expect(conf.get('version')).toEqual(jasmine.stringMatching(/^[\d.]+$/));
    expect(conf.get('api.path')).toBeDefined();
    expect(typeof(conf.get('api.path'))).toEqual('string');
    expect(conf.get('api.host')).toBeUndefined();

});
});
