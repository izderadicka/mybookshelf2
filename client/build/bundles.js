module.exports = {
  "bundles": {
    "dist/app-build": {
      "includes": [
        "[*.js]",
        "[**/*.js]",
        "*.html!text",
        "**/*.html!text",
        "*.json!text",
        "**/*.json!text",
        "*.css!text",
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
        "jquery"

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
