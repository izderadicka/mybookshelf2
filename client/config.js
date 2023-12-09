System.config({
  defaultJSExtensions: true,
  transpiler: false,
  paths: {
    "*": "dist/*",
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },
  map: {
    "aurelia-animator-css": "npm:aurelia-animator-css@1.0.1",
    "aurelia-auth": "npm:aurelia-auth@3.0.4",
    "aurelia-bootstrapper": "npm:aurelia-bootstrapper@1.0.1",
    "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
    "aurelia-dialog": "npm:aurelia-dialog@1.0.0-beta.3.0.1",
    "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
    "aurelia-fetch-client": "npm:aurelia-fetch-client@1.0.1",
    "aurelia-framework": "npm:aurelia-framework@1.0.7",
    "aurelia-history-browser": "npm:aurelia-history-browser@1.0.0",
    "aurelia-loader-default": "npm:aurelia-loader-default@1.0.0",
    "aurelia-logging-console": "npm:aurelia-logging-console@1.0.0",
    "aurelia-pal-browser": "npm:aurelia-pal-browser@1.0.0",
    "aurelia-polyfills": "npm:aurelia-polyfills@1.1.1",
    "aurelia-router": "npm:aurelia-router@1.0.7",
    "aurelia-templating-binding": "npm:aurelia-templating-binding@1.0.0",
    "aurelia-templating-resources": "npm:aurelia-templating-resources@1.1.1",
    "aurelia-templating-router": "npm:aurelia-templating-router@1.0.0",
    "autobahn": "@empty",
    "bluebird": "npm:bluebird@3.4.1",
    "bootstrap": "github:twbs/bootstrap@3.3.7",
    "bootstrap-drawer": "npm:bootstrap-drawer@1.0.6",
    "diacritic": "npm:diacritic@0.0.2",
    "fetch": "github:github/fetch@1.1.0",
    "font-awesome": "npm:font-awesome@4.7.0",
    "izderadicka/asexor_js_client": "github:izderadicka/asexor_js_client@master",
    "jquery": "npm:jquery@2.2.4",
    "select2": "github:select2/select2@4.0.3",
    "text": "github:systemjs/plugin-text@0.0.8",
    "github:jspm/nodelibs-assert@0.1.0": {
      "assert": "npm:assert@1.4.1"
    },
    "github:jspm/nodelibs-buffer@0.1.0": {
      "buffer": "npm:buffer@3.6.0"
    },
    "github:jspm/nodelibs-path@0.1.0": {
      "path-browserify": "npm:path-browserify@0.0.0"
    },
    "github:jspm/nodelibs-process@0.1.2": {
      "process": "npm:process@0.11.9"
    },
    "github:jspm/nodelibs-util@0.1.0": {
      "util": "npm:util@0.10.3"
    },
    "github:jspm/nodelibs-vm@0.1.0": {
      "vm-browserify": "npm:vm-browserify@0.0.4"
    },
    "github:select2/select2@4.0.3": {
      "jquery": "npm:jquery@2.2.4"
    },
    "github:twbs/bootstrap@3.3.7": {
      "jquery": "npm:jquery@2.2.4"
    },
    "npm:assert@1.4.1": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "util": "npm:util@0.10.3"
    },
    "npm:aurelia-animator-css@1.0.1": {
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.2"
    },
    "npm:aurelia-auth@3.0.4": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
      "aurelia-fetch-client": "npm:aurelia-fetch-client@1.0.1",
      "aurelia-router": "npm:aurelia-router@1.0.7"
    },
    "npm:aurelia-binding@1.0.9": {
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.1.0"
    },
    "npm:aurelia-bootstrapper@1.0.1": {
      "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
      "aurelia-framework": "npm:aurelia-framework@1.0.7",
      "aurelia-history": "npm:aurelia-history@1.0.0",
      "aurelia-history-browser": "npm:aurelia-history-browser@1.0.0",
      "aurelia-loader-default": "npm:aurelia-loader-default@1.0.0",
      "aurelia-logging-console": "npm:aurelia-logging-console@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-pal-browser": "npm:aurelia-pal-browser@1.0.0",
      "aurelia-polyfills": "npm:aurelia-polyfills@1.1.1",
      "aurelia-router": "npm:aurelia-router@1.0.7",
      "aurelia-templating": "npm:aurelia-templating@1.1.2",
      "aurelia-templating-binding": "npm:aurelia-templating-binding@1.0.0",
      "aurelia-templating-resources": "npm:aurelia-templating-resources@1.1.1",
      "aurelia-templating-router": "npm:aurelia-templating-router@1.0.0"
    },
    "npm:aurelia-dependency-injection@1.2.0": {
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-dialog@1.0.0-beta.3.0.1": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.2"
    },
    "npm:aurelia-event-aggregator@1.0.0": {
      "aurelia-logging": "npm:aurelia-logging@1.1.1"
    },
    "npm:aurelia-framework@1.0.7": {
      "aurelia-binding": "npm:aurelia-binding@1.0.9",
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.1.1",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.1.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.2"
    },
    "npm:aurelia-history-browser@1.0.0": {
      "aurelia-history": "npm:aurelia-history@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-loader-default@1.0.0": {
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-loader@1.0.0": {
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-path": "npm:aurelia-path@1.1.1"
    },
    "npm:aurelia-logging-console@1.0.0": {
      "aurelia-logging": "npm:aurelia-logging@1.1.1"
    },
    "npm:aurelia-metadata@1.0.2": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-pal-browser@1.0.0": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-polyfills@1.1.1": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-route-recognizer@1.1.0": {
      "aurelia-path": "npm:aurelia-path@1.1.1"
    },
    "npm:aurelia-router@1.0.7": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
      "aurelia-history": "npm:aurelia-history@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-path": "npm:aurelia-path@1.1.1",
      "aurelia-route-recognizer": "npm:aurelia-route-recognizer@1.1.0"
    },
    "npm:aurelia-task-queue@1.1.0": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-templating-binding@1.0.0": {
      "aurelia-binding": "npm:aurelia-binding@1.0.9",
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-templating": "npm:aurelia-templating@1.1.2"
    },
    "npm:aurelia-templating-resources@1.1.1": {
      "aurelia-binding": "npm:aurelia-binding@1.0.9",
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.1.1",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.1.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.2"
    },
    "npm:aurelia-templating-router@1.0.0": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.1.1",
      "aurelia-router": "npm:aurelia-router@1.0.7",
      "aurelia-templating": "npm:aurelia-templating@1.1.2"
    },
    "npm:aurelia-templating@1.1.2": {
      "aurelia-binding": "npm:aurelia-binding@1.0.9",
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.2.0",
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.1.1",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.2",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.1.1",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.1.0"
    },
    "npm:bluebird@3.4.1": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:bootstrap-drawer@1.0.6": {
      "bootstrap": "npm:bootstrap@3.3.7",
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "jquery": "npm:jquery@2.2.4"
    },
    "npm:bootstrap@3.3.7": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:buffer@3.6.0": {
      "base64-js": "npm:base64-js@0.0.8",
      "child_process": "github:jspm/nodelibs-child_process@0.1.0",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "ieee754": "npm:ieee754@1.1.8",
      "isarray": "npm:isarray@1.0.0",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:font-awesome@4.7.0": {
      "css": "github:systemjs/plugin-css@0.1.32"
    },
    "npm:inherits@2.0.1": {
      "util": "github:jspm/nodelibs-util@0.1.0"
    },
    "npm:path-browserify@0.0.0": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:process@0.11.9": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "vm": "github:jspm/nodelibs-vm@0.1.0"
    },
    "npm:util@0.10.3": {
      "inherits": "npm:inherits@2.0.1",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:vm-browserify@0.0.4": {
      "indexof": "npm:indexof@0.0.1"
    }
  },
  bundles: {
    "aurelia.js": [
      "github:github/fetch@1.1.0.js",
      "github:github/fetch@1.1.0/fetch.js",
      "github:izderadicka/asexor_js_client@master.js",
      "github:izderadicka/asexor_js_client@master/lib/base-client.js",
      "github:izderadicka/asexor_js_client@master/lib/client.js",
      "github:izderadicka/asexor_js_client@master/lib/index.js",
      "github:izderadicka/asexor_js_client@master/lib/longpoll-client.js",
      "github:izderadicka/asexor_js_client@master/lib/wamp-client.js",
      "github:select2/select2@4.0.3.js",
      "github:select2/select2@4.0.3/css/select2.css!github:systemjs/plugin-text@0.0.8.js",
      "github:select2/select2@4.0.3/js/select2.js",
      "github:twbs/bootstrap@3.3.7.js",
      "github:twbs/bootstrap@3.3.7/css/bootstrap.css!github:systemjs/plugin-text@0.0.8.js",
      "github:twbs/bootstrap@3.3.7/js/bootstrap.js",
      "npm:aurelia-animator-css@1.0.1.js",
      "npm:aurelia-animator-css@1.0.1/aurelia-animator-css.js",
      "npm:aurelia-auth@3.0.4.js",
      "npm:aurelia-auth@3.0.4/aurelia-auth.js",
      "npm:aurelia-auth@3.0.4/auth-fetch-config.js",
      "npm:aurelia-auth@3.0.4/auth-filter.js",
      "npm:aurelia-auth@3.0.4/auth-service.js",
      "npm:aurelia-auth@3.0.4/auth-utilities.js",
      "npm:aurelia-auth@3.0.4/authentication.js",
      "npm:aurelia-auth@3.0.4/authorize-step.js",
      "npm:aurelia-auth@3.0.4/base-config.js",
      "npm:aurelia-auth@3.0.4/oAuth1.js",
      "npm:aurelia-auth@3.0.4/oAuth2.js",
      "npm:aurelia-auth@3.0.4/popup.js",
      "npm:aurelia-auth@3.0.4/storage.js",
      "npm:aurelia-binding@1.0.9.js",
      "npm:aurelia-binding@1.0.9/aurelia-binding.js",
      "npm:aurelia-bootstrapper@1.0.1.js",
      "npm:aurelia-bootstrapper@1.0.1/aurelia-bootstrapper.js",
      "npm:aurelia-dependency-injection@1.2.0.js",
      "npm:aurelia-dependency-injection@1.2.0/aurelia-dependency-injection.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/ai-dialog-body.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/ai-dialog-footer.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/ai-dialog-header.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/ai-dialog.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/attach-focus.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/aurelia-dialog.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/dialog-configuration.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/dialog-controller.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/dialog-options.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/dialog-renderer.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/dialog-result.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/dialog-service.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/lifecycle.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.1/renderer.js",
      "npm:aurelia-event-aggregator@1.0.0.js",
      "npm:aurelia-event-aggregator@1.0.0/aurelia-event-aggregator.js",
      "npm:aurelia-fetch-client@1.0.1.js",
      "npm:aurelia-fetch-client@1.0.1/aurelia-fetch-client.js",
      "npm:aurelia-framework@1.0.7.js",
      "npm:aurelia-framework@1.0.7/aurelia-framework.js",
      "npm:aurelia-history-browser@1.0.0.js",
      "npm:aurelia-history-browser@1.0.0/aurelia-history-browser.js",
      "npm:aurelia-history@1.0.0.js",
      "npm:aurelia-history@1.0.0/aurelia-history.js",
      "npm:aurelia-loader-default@1.0.0.js",
      "npm:aurelia-loader-default@1.0.0/aurelia-loader-default.js",
      "npm:aurelia-loader@1.0.0.js",
      "npm:aurelia-loader@1.0.0/aurelia-loader.js",
      "npm:aurelia-logging-console@1.0.0.js",
      "npm:aurelia-logging-console@1.0.0/aurelia-logging-console.js",
      "npm:aurelia-logging@1.1.1.js",
      "npm:aurelia-logging@1.1.1/aurelia-logging.js",
      "npm:aurelia-metadata@1.0.2.js",
      "npm:aurelia-metadata@1.0.2/aurelia-metadata.js",
      "npm:aurelia-pal-browser@1.0.0.js",
      "npm:aurelia-pal-browser@1.0.0/aurelia-pal-browser.js",
      "npm:aurelia-pal@1.0.0.js",
      "npm:aurelia-pal@1.0.0/aurelia-pal.js",
      "npm:aurelia-path@1.1.1.js",
      "npm:aurelia-path@1.1.1/aurelia-path.js",
      "npm:aurelia-polyfills@1.1.1.js",
      "npm:aurelia-polyfills@1.1.1/aurelia-polyfills.js",
      "npm:aurelia-route-recognizer@1.1.0.js",
      "npm:aurelia-route-recognizer@1.1.0/aurelia-route-recognizer.js",
      "npm:aurelia-router@1.0.7.js",
      "npm:aurelia-router@1.0.7/aurelia-router.js",
      "npm:aurelia-task-queue@1.1.0.js",
      "npm:aurelia-task-queue@1.1.0/aurelia-task-queue.js",
      "npm:aurelia-templating-binding@1.0.0.js",
      "npm:aurelia-templating-binding@1.0.0/aurelia-templating-binding.js",
      "npm:aurelia-templating-resources@1.1.1.js",
      "npm:aurelia-templating-resources@1.1.1/abstract-repeater.js",
      "npm:aurelia-templating-resources@1.1.1/analyze-view-factory.js",
      "npm:aurelia-templating-resources@1.1.1/array-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.1.1/attr-binding-behavior.js",
      "npm:aurelia-templating-resources@1.1.1/aurelia-hide-style.js",
      "npm:aurelia-templating-resources@1.1.1/aurelia-templating-resources.js",
      "npm:aurelia-templating-resources@1.1.1/binding-mode-behaviors.js",
      "npm:aurelia-templating-resources@1.1.1/binding-signaler.js",
      "npm:aurelia-templating-resources@1.1.1/compose.js",
      "npm:aurelia-templating-resources@1.1.1/css-resource.js",
      "npm:aurelia-templating-resources@1.1.1/debounce-binding-behavior.js",
      "npm:aurelia-templating-resources@1.1.1/dynamic-element.js",
      "npm:aurelia-templating-resources@1.1.1/focus.js",
      "npm:aurelia-templating-resources@1.1.1/hide.js",
      "npm:aurelia-templating-resources@1.1.1/html-resource-plugin.js",
      "npm:aurelia-templating-resources@1.1.1/html-sanitizer.js",
      "npm:aurelia-templating-resources@1.1.1/if.js",
      "npm:aurelia-templating-resources@1.1.1/map-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.1.1/null-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.1.1/number-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.1.1/repeat-strategy-locator.js",
      "npm:aurelia-templating-resources@1.1.1/repeat-utilities.js",
      "npm:aurelia-templating-resources@1.1.1/repeat.js",
      "npm:aurelia-templating-resources@1.1.1/replaceable.js",
      "npm:aurelia-templating-resources@1.1.1/sanitize-html.js",
      "npm:aurelia-templating-resources@1.1.1/set-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.1.1/show.js",
      "npm:aurelia-templating-resources@1.1.1/signal-binding-behavior.js",
      "npm:aurelia-templating-resources@1.1.1/throttle-binding-behavior.js",
      "npm:aurelia-templating-resources@1.1.1/update-trigger-binding-behavior.js",
      "npm:aurelia-templating-resources@1.1.1/with.js",
      "npm:aurelia-templating-router@1.0.0.js",
      "npm:aurelia-templating-router@1.0.0/aurelia-templating-router.js",
      "npm:aurelia-templating-router@1.0.0/route-href.js",
      "npm:aurelia-templating-router@1.0.0/route-loader.js",
      "npm:aurelia-templating-router@1.0.0/router-view.js",
      "npm:aurelia-templating@1.1.2.js",
      "npm:aurelia-templating@1.1.2/aurelia-templating.js",
      "npm:bootstrap-drawer@1.0.6.js",
      "npm:bootstrap-drawer@1.0.6/dist/css/bootstrap-drawer.css!github:systemjs/plugin-text@0.0.8.js",
      "npm:bootstrap-drawer@1.0.6/js/drawer.js",
      "npm:diacritic@0.0.2.js",
      "npm:diacritic@0.0.2/diacritics.js",
      "npm:font-awesome@4.7.0/css/font-awesome.css!github:systemjs/plugin-text@0.0.8.js",
      "npm:jquery@2.2.4.js",
      "npm:jquery@2.2.4/dist/jquery.js"
    ],
    "app-build.js": [
      "app.html!github:systemjs/plugin-text@0.0.8.js",
      "app.js",
      "components/add-to-shelf-button.html!github:systemjs/plugin-text@0.0.8.js",
      "components/add-to-shelf-button.js",
      "components/author.html!github:systemjs/plugin-text@0.0.8.js",
      "components/author.js",
      "components/authors-converter.js",
      "components/authors-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "components/authors-edit.js",
      "components/authors.html!github:systemjs/plugin-text@0.0.8.js",
      "components/authors.js",
      "components/autocomplete/autocomplete-authors.html!github:systemjs/plugin-text@0.0.8.js",
      "components/autocomplete/autocomplete-ebooks.html!github:systemjs/plugin-text@0.0.8.js",
      "components/autocomplete/autocomplete-series.html!github:systemjs/plugin-text@0.0.8.js",
      "components/autocomplete/autocomplete.css!github:systemjs/plugin-text@0.0.8.js",
      "components/autocomplete/autocomplete.html!github:systemjs/plugin-text@0.0.8.js",
      "components/autocomplete/autocomplete.js",
      "components/base-card.js",
      "components/blur-image.js",
      "components/confirm-dialog.html!github:systemjs/plugin-text@0.0.8.js",
      "components/confirm-dialog.js",
      "components/context-menu/context-menu.css!github:systemjs/plugin-text@0.0.8.js",
      "components/context-menu/context-menu.html!github:systemjs/plugin-text@0.0.8.js",
      "components/context-menu/context-menu.js",
      "components/cover.html!github:systemjs/plugin-text@0.0.8.js",
      "components/cover.js",
      "components/date-converter.js",
      "components/ebook-action-list.html!github:systemjs/plugin-text@0.0.8.js",
      "components/ebook-action-list.js",
      "components/ebook-card.html!github:systemjs/plugin-text@0.0.8.js",
      "components/ebook-card.js",
      "components/ebook-panel.html!github:systemjs/plugin-text@0.0.8.js",
      "components/ebook-panel.js",
      "components/ebook-tiles.html!github:systemjs/plugin-text@0.0.8.js",
      "components/ebook-tiles.js",
      "components/edit-buttons.html!github:systemjs/plugin-text@0.0.8.js",
      "components/edit-buttons.js",
      "components/error-alert.html!github:systemjs/plugin-text@0.0.8.js",
      "components/error-alert.js",
      "components/genres-converter.js",
      "components/genres-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "components/genres-edit.js",
      "components/genres-select.html!github:systemjs/plugin-text@0.0.8.js",
      "components/genres-select.js",
      "components/int-converter.js",
      "components/list-converter.js",
      "components/merge-direction.html!github:systemjs/plugin-text@0.0.8.js",
      "components/merge-direction.js",
      "components/nav-bar.html!github:systemjs/plugin-text@0.0.8.js",
      "components/nav-bar.js",
      "components/notification-base.js",
      "components/notification-convert-many.html!github:systemjs/plugin-text@0.0.8.js",
      "components/notification-convert-many.js",
      "components/notification-convert.html!github:systemjs/plugin-text@0.0.8.js",
      "components/notification-convert.js",
      "components/notification-cover.html!github:systemjs/plugin-text@0.0.8.js",
      "components/notification-cover.js",
      "components/notification-metadata.html!github:systemjs/plugin-text@0.0.8.js",
      "components/notification-metadata.js",
      "components/notifications-drawer.html!github:systemjs/plugin-text@0.0.8.js",
      "components/notifications-drawer.js",
      "components/pagination/index.js",
      "components/pagination/page-controller.js",
      "components/pagination/pager.html!github:systemjs/plugin-text@0.0.8.js",
      "components/pagination/pager.js",
      "components/pagination/sorter.html!github:systemjs/plugin-text@0.0.8.js",
      "components/pagination/sorter.js",
      "components/rating/rating.css!github:systemjs/plugin-text@0.0.8.js",
      "components/rating/rating.html!github:systemjs/plugin-text@0.0.8.js",
      "components/rating/rating.js",
      "components/search.html!github:systemjs/plugin-text@0.0.8.js",
      "components/search.js",
      "components/series-card.html!github:systemjs/plugin-text@0.0.8.js",
      "components/series-card.js",
      "components/size-converter.js",
      "components/slice-converter.js",
      "config.js",
      "lib/access.js",
      "lib/api-client.js",
      "lib/application-state.js",
      "lib/config/config.js",
      "lib/config/index.js",
      "lib/notification.js",
      "lib/pidi-cache.js",
      "lib/utils.js",
      "lib/ws-client.js",
      "main.js",
      "models/author.js",
      "models/base-model.js",
      "models/bookshelf-item.js",
      "models/bookshelf.js",
      "models/ebook.js",
      "models/series.js",
      "pages/abstract/convert-many.js",
      "pages/abstract/edit.js",
      "pages/abstract/merge.js",
      "pages/author-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/author-edit.js",
      "pages/author-merge.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/author-merge.js",
      "pages/author.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/author.js",
      "pages/batch-conversions.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/batch-conversions.js",
      "pages/conversions.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/conversions.js",
      "pages/cover-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/cover-edit.js",
      "pages/ebook-add-to-shelf.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook-add-to-shelf.js",
      "pages/ebook-conversions.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook-conversions.js",
      "pages/ebook-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook-edit.js",
      "pages/ebook-merge.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook-merge.js",
      "pages/ebook.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook.js",
      "pages/ebooks.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebooks.js",
      "pages/login.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/login.js",
      "pages/profile.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/profile.js",
      "pages/search.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/search.js",
      "pages/series-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/series-edit.js",
      "pages/series-merge.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/series-merge.js",
      "pages/series.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/series.js",
      "pages/shelf-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/shelf-edit.js",
      "pages/shelf-item-edit-dialog.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/shelf-item-edit-dialog.js",
      "pages/shelf-merge.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/shelf-merge.js",
      "pages/shelf.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/shelf.js",
      "pages/shelves.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/shelves.js",
      "pages/source-move.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/source-move.js",
      "pages/upload-result.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/upload-result.js",
      "pages/upload.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/upload.js",
      "pages/welcome.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/welcome.js",
      "pub-app.html!github:systemjs/plugin-text@0.0.8.js",
      "pub-app.js",
      "routes.js",
      "test/test-page.html!github:systemjs/plugin-text@0.0.8.js",
      "test/test-page.js"
    ]
  },
  depCache: {
    "app.js": [
      "aurelia-auth",
      "aurelia-framework",
      "aurelia-fetch-client",
      "lib/config/index",
      "lib/ws-client",
      "lib/access",
      "routes",
      "components/confirm-dialog",
      "aurelia-dialog",
      "aurelia-event-aggregator"
    ],
    "components/add-to-shelf-button.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client"
    ],
    "components/author.js": [
      "aurelia-framework"
    ],
    "components/authors-edit.js": [
      "aurelia-framework",
      "lib/api-client",
      "jquery"
    ],
    "components/authors.js": [
      "aurelia-framework"
    ],
    "components/autocomplete/autocomplete.js": [
      "aurelia-framework",
      "jquery",
      "diacritic",
      "lib/utils"
    ],
    "components/blur-image.js": [
      "aurelia-framework"
    ],
    "components/confirm-dialog.js": [
      "aurelia-framework",
      "aurelia-dialog"
    ],
    "components/context-menu/context-menu.js": [
      "aurelia-framework",
      "jquery"
    ],
    "components/cover.js": [
      "aurelia-framework",
      "jquery"
    ],
    "components/date-converter.js": [
      "aurelia-framework",
      "lib/config/index"
    ],
    "components/ebook-action-list.js": [
      "aurelia-framework"
    ],
    "components/ebook-card.js": [
      "aurelia-framework",
      "aurelia-fetch-client",
      "jquery",
      "./base-card"
    ],
    "components/ebook-panel.js": [
      "aurelia-framework",
      "aurelia-fetch-client",
      "jquery"
    ],
    "components/ebook-tiles.js": [
      "aurelia-framework",
      "aurelia-fetch-client",
      "lib/api-client",
      "components/authors-converter",
      "jquery"
    ],
    "components/edit-buttons.js": [
      "aurelia-framework"
    ],
    "components/error-alert.js": [
      "aurelia-framework"
    ],
    "components/genres-edit.js": [
      "aurelia-framework"
    ],
    "components/genres-select.js": [
      "aurelia-framework",
      "lib/api-client",
      "jquery",
      "select2",
      "lib/utils"
    ],
    "components/merge-direction.js": [
      "aurelia-framework"
    ],
    "components/nav-bar.js": [
      "aurelia-framework",
      "lib/access",
      "lib/ws-client",
      "jquery"
    ],
    "components/notification-base.js": [
      "aurelia-framework",
      "aurelia-router",
      "components/notifications-drawer"
    ],
    "components/notification-convert-many.js": [
      "./notification-base"
    ],
    "components/notification-convert.js": [
      "./notification-base"
    ],
    "components/notification-cover.js": [
      "./notification-base"
    ],
    "components/notification-metadata.js": [
      "./notification-base"
    ],
    "components/notifications-drawer.js": [
      "lib/notification",
      "aurelia-framework",
      "lib/config/index",
      "jquery"
    ],
    "components/pagination/page-controller.js": [
      "aurelia-framework"
    ],
    "components/pagination/pager.js": [
      "aurelia-framework"
    ],
    "components/pagination/sorter.js": [
      "aurelia-framework"
    ],
    "components/rating/rating.js": [
      "aurelia-framework"
    ],
    "components/search.js": [
      "aurelia-framework",
      "jquery"
    ],
    "components/series-card.js": [
      "aurelia-framework",
      "./base-card"
    ],
    "components/size-converter.js": [
      "aurelia-framework",
      "lib/config/index"
    ],
    "lib/access.js": [
      "aurelia-auth",
      "aurelia-auth/authentication",
      "aurelia-framework",
      "aurelia-event-aggregator",
      "aurelia-router",
      "aurelia-fetch-client"
    ],
    "lib/api-client.js": [
      "aurelia-fetch-client",
      "aurelia-framework",
      "bootstrap",
      "lib/config/index",
      "./pidi-cache"
    ],
    "lib/config/config.js": [
      "aurelia-framework"
    ],
    "lib/config/index.js": [
      "./config",
      "aurelia-framework"
    ],
    "lib/notification.js": [
      "aurelia-framework",
      "lib/config/index",
      "aurelia-event-aggregator"
    ],
    "lib/ws-client.js": [
      "lib/notification",
      "lib/access",
      "aurelia-framework",
      "lib/config/index",
      "aurelia-event-aggregator",
      "izderadicka/asexor_js_client"
    ],
    "main.js": [
      "bootstrap",
      "bootstrap-drawer",
      "config"
    ],
    "models/author.js": [
      "./base-model"
    ],
    "models/base-model.js": [
      "aurelia-framework",
      "aurelia-dependency-injection"
    ],
    "models/bookshelf-item.js": [
      "./base-model"
    ],
    "models/bookshelf.js": [
      "./base-model"
    ],
    "models/ebook.js": [
      "aurelia-framework",
      "aurelia-dependency-injection",
      "./base-model"
    ],
    "models/series.js": [
      "./base-model"
    ],
    "pages/abstract/convert-many.js": [
      "aurelia-framework"
    ],
    "pages/abstract/edit.js": [
      "components/confirm-dialog",
      "aurelia-framework"
    ],
    "pages/abstract/merge.js": [
      "aurelia-framework"
    ],
    "pages/author-edit.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "models/author",
      "aurelia-dialog",
      "./abstract/edit"
    ],
    "pages/author-merge.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "./abstract/merge"
    ],
    "pages/author.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/utils",
      "lib/access",
      "aurelia-router",
      "lib/config/index",
      "lib/ws-client",
      "./abstract/convert-many"
    ],
    "pages/batch-conversions.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/access"
    ],
    "pages/conversions.js": [
      "aurelia-framework"
    ],
    "pages/cover-edit.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/ws-client",
      "aurelia-router",
      "aurelia-event-aggregator",
      "jquery"
    ],
    "pages/ebook-add-to-shelf.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client"
    ],
    "pages/ebook-conversions.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/access"
    ],
    "pages/ebook-edit.js": [
      "aurelia-framework",
      "aurelia-router",
      "jquery",
      "lib/api-client",
      "lib/access",
      "models/ebook",
      "aurelia-dialog",
      "./abstract/edit"
    ],
    "pages/ebook-merge.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "./abstract/merge"
    ],
    "pages/ebook.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/access",
      "aurelia-dialog",
      "components/confirm-dialog",
      "lib/ws-client",
      "aurelia-event-aggregator",
      "aurelia-router",
      "./source-move",
      "lib/config/index"
    ],
    "pages/ebooks.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/utils"
    ],
    "pages/login.js": [
      "lib/access",
      "aurelia-framework",
      "aurelia-router"
    ],
    "pages/profile.js": [
      "aurelia-framework",
      "lib/access"
    ],
    "pages/search.js": [
      "aurelia-framework",
      "lib/api-client"
    ],
    "pages/series-edit.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "models/series",
      "aurelia-dialog",
      "./abstract/edit"
    ],
    "pages/series-merge.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "./abstract/merge"
    ],
    "pages/series.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/access",
      "aurelia-router",
      "lib/config/index",
      "./abstract/convert-many",
      "lib/ws-client"
    ],
    "pages/shelf-edit.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "models/ebook",
      "aurelia-dialog",
      "./abstract/edit",
      "models/bookshelf"
    ],
    "pages/shelf-item-edit-dialog.js": [
      "aurelia-framework",
      "aurelia-dialog",
      "models/bookshelf-item",
      "lib/api-client"
    ],
    "pages/shelf-merge.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "./abstract/merge"
    ],
    "pages/shelf.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/access",
      "aurelia-router",
      "aurelia-dialog",
      "./shelf-item-edit-dialog",
      "components/confirm-dialog",
      "./abstract/convert-many",
      "lib/ws-client",
      "lib/config/index"
    ],
    "pages/shelves.js": [
      "aurelia-framework",
      "lib/api-client"
    ],
    "pages/source-move.js": [
      "aurelia-framework",
      "aurelia-router",
      "lib/api-client",
      "lib/access",
      "aurelia-dialog"
    ],
    "pages/upload-result.js": [
      "aurelia-framework",
      "lib/api-client",
      "aurelia-router"
    ],
    "pages/upload.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/config/index",
      "lib/ws-client",
      "aurelia-event-aggregator",
      "lib/notification",
      "aurelia-router"
    ],
    "pages/welcome.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/utils"
    ],
    "test/test-page.js": [
      "aurelia-framework",
      "lib/api-client"
    ]
  }
});