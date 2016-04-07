import  'bootstrap';
import {ApplicationState} from 'lib/application-state'
import authConfig from './authConfig';

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    .developmentLogging()
    .instance(ApplicationState, new ApplicationState())
    .feature('components/pagination')
    .plugin('aurelia-auth', baseConfig => baseConfig.configure(authConfig));


  //Uncomment the line below to enable animation.
  //aurelia.use.plugin('aurelia-animator-css');
  //if the css animator is enabled, add swap-order="after" to all router-view elements

  //Anyone wanting to use HTMLImports to load views, will need to install the following plugin.
  //aurelia.use.plugin('aurelia-html-import-template-loader')

  aurelia.start().then(() => aurelia.setRoot('app'));
}
