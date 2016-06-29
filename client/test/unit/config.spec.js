import {Configure} from 'lib/config/index';
import {DefaultLoader} from 'aurelia-loader-default';


describe('When using Configure', () => {

let loader = new DefaultLoader();
var conf = null;

beforeEach(() => {
  conf = new Configure(loader);
})
it('it should contain default instance properties', () => {
expect(conf._config).toBeDefined();
expect(conf.loader).not.toBeNull();
expect(conf.loader).not.toBeNull();
});

it('it should load config with values', (done) =>{
  conf.loadFile().then(() => {
    expect(conf.get('version')).toEqual(jasmine.stringMatching(/^[\d.]+$/));
    expect(conf.get('api.host')).toBeDefined();
    expect(typeof(conf.get('api.host'))).toEqual('string');
    done();
  });
});
});
