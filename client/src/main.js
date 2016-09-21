import  'bootstrap';
import 'bootstrap-drawer';
import config from 'config';
import env from 'environment';

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    .feature('components/pagination')
    .plugin('aurelia-auth', baseConfig => baseConfig.configure(config.authentication))
    .feature('lib/config', conf => conf.configure(config))
    .plugin('aurelia-dialog', config => {
      config.useDefaults();
      config.settings.lock = false;
      config.settings.centerHorizontalOnly = false;
      config.settings.startingZIndex = 1045;
    });
    //.plugin('aurelia-configuration');

  if (env.debug) aurelia.use.developmentLogging();





  //Uncomment the line below to enable animation.
  //aurelia.use.plugin('aurelia-animator-css');
  //if the css animator is enabled, add swap-order="after" to all router-view elements

  //Anyone wanting to use HTMLImports to load views, will need to install the following plugin.
  //aurelia.use.plugin('aurelia-html-import-template-loader')

  aurelia.start().then(() => aurelia.setRoot('app'));
}
