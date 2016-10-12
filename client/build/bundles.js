module.exports = {
  "bundles": {
    "dist/app-build": {
      "includes": [
        "[**/*.js]",
        "**/*.html!text",
        "**/*.json!text",
        "**/*.css!text"
      ],
      "options": {
        "inject": true,
        "minify": true,
        "depCache": true,
        "rev": false
      }
    },
    "dist/aurelia": {
      "includes": [
        "aurelia-framework",
        "aurelia-bootstrapper",
        "aurelia-fetch-client",
        "aurelia-router",
        "aurelia-animator-css",
        "aurelia-templating-binding",
        "aurelia-polyfills",
        "aurelia-templating-resources",
        "aurelia-templating-router",
        "aurelia-loader-default",
        "aurelia-history-browser",
        "aurelia-logging-console",
        "aurelia-auth",
        "aurelia-dialog",
        "bootstrap-drawer",
        "bootstrap",
        "bootstrap/css/bootstrap.css!text",
        "bootstrap-drawer/dist/css/bootstrap-drawer.css!text",
        "font-awesome/css/font-awesome.css!text",
        "diacritic",
        "fetch",
        "jquery",
        "select2",
        "select2/css/select2.css!text"
      ],
      "options": {
        "inject": true,
        "minify": true,
        "depCache": false,
        "rev": false
      }
    }
/*
    ,

    "dist/bootstrap": {
      "includes": [
        "bootstrap",
        "bootstrap/css/bootstrap.css!text",
        "jquery"
      ],
      "options": {
        "inject": true,
        "minify": true,
        "depCache": false,
        "rev": false
      }
    }
*/
  }
};
