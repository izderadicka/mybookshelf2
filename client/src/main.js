import  'bootstrap';
import 'bootstrap-drawer/dist/js/drawer';
import authConfig from 'config/auth-config';

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    .developmentLogging()
    .feature('components/pagination')
    .plugin('aurelia-auth', baseConfig => baseConfig.configure(authConfig))
    .feature('lib/config')
    .plugin('aurelia-dialog', config => {
      config.useDefaults();
      config.settings.lock = false;
      config.settings.centerHorizontalOnly = false;
      config.settings.startingZIndex = 1045;
    });
    //.plugin('aurelia-configuration');



  //Uncomment the line below to enable animation.
  //aurelia.use.plugin('aurelia-animator-css');
  //if the css animator is enabled, add swap-order="after" to all router-view elements

  //Anyone wanting to use HTMLImports to load views, will need to install the following plugin.
  //aurelia.use.plugin('aurelia-html-import-template-loader')

  aurelia.start().then(() => aurelia.setRoot('app'));
}
