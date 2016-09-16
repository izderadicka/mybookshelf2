System.config({
  defaultJSExtensions: true,
  transpiler: false,
  paths: {
    "*": "dist/*",
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },
  map: {
    "aurelia-animator-css": "npm:aurelia-animator-css@1.0.0",
    "aurelia-auth": "npm:aurelia-auth@3.0.2",
    "aurelia-bootstrapper": "npm:aurelia-bootstrapper@1.0.0",
    "aurelia-dialog": "npm:aurelia-dialog@1.0.0-beta.3.0.0",
    "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
    "aurelia-fetch-client": "npm:aurelia-fetch-client@1.0.0",
    "aurelia-framework": "npm:aurelia-framework@1.0.0",
    "aurelia-history-browser": "npm:aurelia-history-browser@1.0.0",
    "aurelia-loader-default": "npm:aurelia-loader-default@1.0.0",
    "aurelia-logging-console": "npm:aurelia-logging-console@1.0.0",
    "aurelia-pal-browser": "npm:aurelia-pal-browser@1.0.0",
    "aurelia-polyfills": "npm:aurelia-polyfills@1.0.0",
    "aurelia-router": "npm:aurelia-router@1.0.3",
    "aurelia-templating-binding": "npm:aurelia-templating-binding@1.0.0",
    "aurelia-templating-resources": "npm:aurelia-templating-resources@1.0.0",
    "aurelia-templating-router": "npm:aurelia-templating-router@1.0.0",
    "bluebird": "npm:bluebird@3.4.1",
    "bootstrap": "github:twbs/bootstrap@3.3.7",
    "bootstrap-drawer": "npm:bootstrap-drawer@1.0.6",
    "diacritic": "npm:diacritic@0.0.2",
    "fetch": "github:github/fetch@1.0.0",
    "font-awesome": "npm:font-awesome@4.6.3",
    "jquery": "npm:jquery@2.2.4",
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
    "github:twbs/bootstrap@3.3.7": {
      "jquery": "npm:jquery@2.2.4"
    },
    "npm:assert@1.4.1": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "util": "npm:util@0.10.3"
    },
    "npm:aurelia-animator-css@1.0.0": {
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.0"
    },
    "npm:aurelia-auth@3.0.2": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
      "aurelia-fetch-client": "npm:aurelia-fetch-client@1.0.0",
      "aurelia-router": "npm:aurelia-router@1.0.3"
    },
    "npm:aurelia-binding@1.0.4": {
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.0.0"
    },
    "npm:aurelia-bootstrapper@1.0.0": {
      "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
      "aurelia-framework": "npm:aurelia-framework@1.0.0",
      "aurelia-history": "npm:aurelia-history@1.0.0",
      "aurelia-history-browser": "npm:aurelia-history-browser@1.0.0",
      "aurelia-loader-default": "npm:aurelia-loader-default@1.0.0",
      "aurelia-logging-console": "npm:aurelia-logging-console@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-pal-browser": "npm:aurelia-pal-browser@1.0.0",
      "aurelia-polyfills": "npm:aurelia-polyfills@1.0.0",
      "aurelia-router": "npm:aurelia-router@1.0.3",
      "aurelia-templating": "npm:aurelia-templating@1.1.0",
      "aurelia-templating-binding": "npm:aurelia-templating-binding@1.0.0",
      "aurelia-templating-resources": "npm:aurelia-templating-resources@1.0.0",
      "aurelia-templating-router": "npm:aurelia-templating-router@1.0.0"
    },
    "npm:aurelia-dependency-injection@1.0.0": {
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-dialog@1.0.0-beta.3.0.0": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.0"
    },
    "npm:aurelia-event-aggregator@1.0.0": {
      "aurelia-logging": "npm:aurelia-logging@1.0.0"
    },
    "npm:aurelia-framework@1.0.0": {
      "aurelia-binding": "npm:aurelia-binding@1.0.4",
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.0.0",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.0"
    },
    "npm:aurelia-history-browser@1.0.0": {
      "aurelia-history": "npm:aurelia-history@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-loader-default@1.0.0": {
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-loader@1.0.0": {
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.0.0"
    },
    "npm:aurelia-logging-console@1.0.0": {
      "aurelia-logging": "npm:aurelia-logging@1.0.0"
    },
    "npm:aurelia-metadata@1.0.0": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-pal-browser@1.0.0": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-polyfills@1.0.0": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-route-recognizer@1.0.0": {
      "aurelia-path": "npm:aurelia-path@1.0.0"
    },
    "npm:aurelia-router@1.0.3": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-event-aggregator": "npm:aurelia-event-aggregator@1.0.0",
      "aurelia-history": "npm:aurelia-history@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.0.0",
      "aurelia-route-recognizer": "npm:aurelia-route-recognizer@1.0.0"
    },
    "npm:aurelia-task-queue@1.0.0": {
      "aurelia-pal": "npm:aurelia-pal@1.0.0"
    },
    "npm:aurelia-templating-binding@1.0.0": {
      "aurelia-binding": "npm:aurelia-binding@1.0.4",
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.0"
    },
    "npm:aurelia-templating-resources@1.0.0": {
      "aurelia-binding": "npm:aurelia-binding@1.0.4",
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.0.0",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.0.0",
      "aurelia-templating": "npm:aurelia-templating@1.1.0"
    },
    "npm:aurelia-templating-router@1.0.0": {
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.0.0",
      "aurelia-router": "npm:aurelia-router@1.0.3",
      "aurelia-templating": "npm:aurelia-templating@1.1.0"
    },
    "npm:aurelia-templating@1.1.0": {
      "aurelia-binding": "npm:aurelia-binding@1.0.4",
      "aurelia-dependency-injection": "npm:aurelia-dependency-injection@1.0.0",
      "aurelia-loader": "npm:aurelia-loader@1.0.0",
      "aurelia-logging": "npm:aurelia-logging@1.0.0",
      "aurelia-metadata": "npm:aurelia-metadata@1.0.0",
      "aurelia-pal": "npm:aurelia-pal@1.0.0",
      "aurelia-path": "npm:aurelia-path@1.0.0",
      "aurelia-task-queue": "npm:aurelia-task-queue@1.0.0"
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
      "ieee754": "npm:ieee754@1.1.6",
      "isarray": "npm:isarray@1.0.0",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:font-awesome@4.6.3": {
      "css": "github:systemjs/plugin-css@0.1.25"
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
      "github:github/fetch@1.0.0.js",
      "github:github/fetch@1.0.0/fetch.js",
      "github:twbs/bootstrap@3.3.7.js",
      "github:twbs/bootstrap@3.3.7/css/bootstrap.css!github:systemjs/plugin-text@0.0.8.js",
      "github:twbs/bootstrap@3.3.7/js/bootstrap.js",
      "npm:aurelia-animator-css@1.0.0.js",
      "npm:aurelia-animator-css@1.0.0/aurelia-animator-css.js",
      "npm:aurelia-auth@3.0.2.js",
      "npm:aurelia-auth@3.0.2/aurelia-auth.js",
      "npm:aurelia-auth@3.0.2/auth-fetch-config.js",
      "npm:aurelia-auth@3.0.2/auth-filter.js",
      "npm:aurelia-auth@3.0.2/auth-service.js",
      "npm:aurelia-auth@3.0.2/auth-utilities.js",
      "npm:aurelia-auth@3.0.2/authentication.js",
      "npm:aurelia-auth@3.0.2/authorize-step.js",
      "npm:aurelia-auth@3.0.2/base-config.js",
      "npm:aurelia-auth@3.0.2/oAuth1.js",
      "npm:aurelia-auth@3.0.2/oAuth2.js",
      "npm:aurelia-auth@3.0.2/popup.js",
      "npm:aurelia-auth@3.0.2/storage.js",
      "npm:aurelia-binding@1.0.4.js",
      "npm:aurelia-binding@1.0.4/aurelia-binding.js",
      "npm:aurelia-bootstrapper@1.0.0.js",
      "npm:aurelia-bootstrapper@1.0.0/aurelia-bootstrapper.js",
      "npm:aurelia-dependency-injection@1.0.0.js",
      "npm:aurelia-dependency-injection@1.0.0/aurelia-dependency-injection.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/ai-dialog-body.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/ai-dialog-footer.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/ai-dialog-header.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/ai-dialog.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/attach-focus.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/aurelia-dialog.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/dialog-configuration.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/dialog-controller.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/dialog-options.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/dialog-renderer.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/dialog-result.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/dialog-service.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/lifecycle.js",
      "npm:aurelia-dialog@1.0.0-beta.3.0.0/renderer.js",
      "npm:aurelia-event-aggregator@1.0.0.js",
      "npm:aurelia-event-aggregator@1.0.0/aurelia-event-aggregator.js",
      "npm:aurelia-fetch-client@1.0.0.js",
      "npm:aurelia-fetch-client@1.0.0/aurelia-fetch-client.js",
      "npm:aurelia-framework@1.0.0.js",
      "npm:aurelia-framework@1.0.0/aurelia-framework.js",
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
      "npm:aurelia-logging@1.0.0.js",
      "npm:aurelia-logging@1.0.0/aurelia-logging.js",
      "npm:aurelia-metadata@1.0.0.js",
      "npm:aurelia-metadata@1.0.0/aurelia-metadata.js",
      "npm:aurelia-pal-browser@1.0.0.js",
      "npm:aurelia-pal-browser@1.0.0/aurelia-pal-browser.js",
      "npm:aurelia-pal@1.0.0.js",
      "npm:aurelia-pal@1.0.0/aurelia-pal.js",
      "npm:aurelia-path@1.0.0.js",
      "npm:aurelia-path@1.0.0/aurelia-path.js",
      "npm:aurelia-polyfills@1.0.0.js",
      "npm:aurelia-polyfills@1.0.0/aurelia-polyfills.js",
      "npm:aurelia-route-recognizer@1.0.0.js",
      "npm:aurelia-route-recognizer@1.0.0/aurelia-route-recognizer.js",
      "npm:aurelia-router@1.0.3.js",
      "npm:aurelia-router@1.0.3/aurelia-router.js",
      "npm:aurelia-task-queue@1.0.0.js",
      "npm:aurelia-task-queue@1.0.0/aurelia-task-queue.js",
      "npm:aurelia-templating-binding@1.0.0.js",
      "npm:aurelia-templating-binding@1.0.0/aurelia-templating-binding.js",
      "npm:aurelia-templating-resources@1.0.0.js",
      "npm:aurelia-templating-resources@1.0.0/abstract-repeater.js",
      "npm:aurelia-templating-resources@1.0.0/analyze-view-factory.js",
      "npm:aurelia-templating-resources@1.0.0/array-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.0.0/aurelia-hide-style.js",
      "npm:aurelia-templating-resources@1.0.0/aurelia-templating-resources.js",
      "npm:aurelia-templating-resources@1.0.0/binding-mode-behaviors.js",
      "npm:aurelia-templating-resources@1.0.0/binding-signaler.js",
      "npm:aurelia-templating-resources@1.0.0/compose.js",
      "npm:aurelia-templating-resources@1.0.0/css-resource.js",
      "npm:aurelia-templating-resources@1.0.0/debounce-binding-behavior.js",
      "npm:aurelia-templating-resources@1.0.0/dynamic-element.js",
      "npm:aurelia-templating-resources@1.0.0/focus.js",
      "npm:aurelia-templating-resources@1.0.0/hide.js",
      "npm:aurelia-templating-resources@1.0.0/html-resource-plugin.js",
      "npm:aurelia-templating-resources@1.0.0/html-sanitizer.js",
      "npm:aurelia-templating-resources@1.0.0/if.js",
      "npm:aurelia-templating-resources@1.0.0/map-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.0.0/null-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.0.0/number-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.0.0/repeat-strategy-locator.js",
      "npm:aurelia-templating-resources@1.0.0/repeat-utilities.js",
      "npm:aurelia-templating-resources@1.0.0/repeat.js",
      "npm:aurelia-templating-resources@1.0.0/replaceable.js",
      "npm:aurelia-templating-resources@1.0.0/sanitize-html.js",
      "npm:aurelia-templating-resources@1.0.0/set-repeat-strategy.js",
      "npm:aurelia-templating-resources@1.0.0/show.js",
      "npm:aurelia-templating-resources@1.0.0/signal-binding-behavior.js",
      "npm:aurelia-templating-resources@1.0.0/throttle-binding-behavior.js",
      "npm:aurelia-templating-resources@1.0.0/update-trigger-binding-behavior.js",
      "npm:aurelia-templating-resources@1.0.0/with.js",
      "npm:aurelia-templating-router@1.0.0.js",
      "npm:aurelia-templating-router@1.0.0/aurelia-templating-router.js",
      "npm:aurelia-templating-router@1.0.0/route-href.js",
      "npm:aurelia-templating-router@1.0.0/route-loader.js",
      "npm:aurelia-templating-router@1.0.0/router-view.js",
      "npm:aurelia-templating@1.1.0.js",
      "npm:aurelia-templating@1.1.0/aurelia-templating.js",
      "npm:bootstrap-drawer@1.0.6.js",
      "npm:bootstrap-drawer@1.0.6/dist/css/bootstrap-drawer.css!github:systemjs/plugin-text@0.0.8.js",
      "npm:bootstrap-drawer@1.0.6/js/drawer.js",
      "npm:font-awesome@4.6.3/css/font-awesome.css!github:systemjs/plugin-text@0.0.8.js",
      "npm:jquery@2.2.4.js",
      "npm:jquery@2.2.4/dist/jquery.js"
    ],
    "app-build.js": [
      "app.html!github:systemjs/plugin-text@0.0.8.js",
      "app.js",
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
      "components/blur-image.js",
      "components/confirm-dialog.html!github:systemjs/plugin-text@0.0.8.js",
      "components/confirm-dialog.js",
      "components/context-menu/context-menu.css!github:systemjs/plugin-text@0.0.8.js",
      "components/context-menu/context-menu.html!github:systemjs/plugin-text@0.0.8.js",
      "components/context-menu/context-menu.js",
      "components/ebook-action-list.html!github:systemjs/plugin-text@0.0.8.js",
      "components/ebook-action-list.js",
      "components/ebook-panel.html!github:systemjs/plugin-text@0.0.8.js",
      "components/ebook-panel.js",
      "components/error-alert.html!github:systemjs/plugin-text@0.0.8.js",
      "components/error-alert.js",
      "components/genres-converter.js",
      "components/genres-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "components/genres-edit.js",
      "components/list-converter.js",
      "components/nav-bar.html!github:systemjs/plugin-text@0.0.8.js",
      "components/nav-bar.js",
      "components/notification-base.js",
      "components/notification-convert.html!github:systemjs/plugin-text@0.0.8.js",
      "components/notification-convert.js",
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
      "config/auth-config.js",
      "config/config.js",
      "lib/access.js",
      "lib/api-client.js",
      "lib/application-state.js",
      "lib/config/config.js",
      "lib/config/index.js",
      "lib/notification.js",
      "lib/ws-client.js",
      "main.js",
      "mins/autobahn.min.js",
      "models/ebook.js",
      "pages/author.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/author.js",
      "pages/ebook-edit.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook-edit.js",
      "pages/ebook.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebook.js",
      "pages/ebooks.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/ebooks.js",
      "pages/login.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/login.js",
      "pages/search.html!github:systemjs/plugin-text@0.0.8.js",
      "pages/search.js",
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
      "routes"
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
      "diacritic"
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
    "components/ebook-action-list.js": [
      "aurelia-framework"
    ],
    "components/ebook-panel.js": [
      "aurelia-framework",
      "aurelia-fetch-client",
      "jquery"
    ],
    "components/error-alert.js": [
      "aurelia-framework"
    ],
    "components/genres-edit.js": [
      "aurelia-framework"
    ],
    "components/nav-bar.js": [
      "aurelia-framework",
      "lib/access",
      "jquery"
    ],
    "components/notification-base.js": [
      "aurelia-framework",
      "aurelia-router"
    ],
    "components/notification-convert.js": [
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
      "aurelia-framework"
    ],
    "lib/access.js": [
      "aurelia-auth",
      "aurelia-auth/authentication",
      "aurelia-framework",
      "aurelia-event-aggregator",
      "aurelia-router"
    ],
    "lib/api-client.js": [
      "aurelia-fetch-client",
      "aurelia-framework",
      "bootstrap",
      "lib/config/index"
    ],
    "lib/config/config.js": [
      "aurelia-framework",
      "config/config"
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
      "mins/autobahn.min"
    ],
    "main.js": [
      "bootstrap",
      "bootstrap-drawer",
      "config/auth-config"
    ],
    "models/ebook.js": [
      "aurelia-framework",
      "aurelia-dependency-injection"
    ],
    "pages/author.js": [
      "aurelia-framework",
      "lib/api-client"
    ],
    "pages/ebook-edit.js": [
      "aurelia-framework",
      "aurelia-router",
      "jquery",
      "lib/api-client",
      "lib/access",
      "models/ebook",
      "aurelia-dialog",
      "components/confirm-dialog"
    ],
    "pages/ebook.js": [
      "aurelia-framework",
      "lib/api-client",
      "lib/access",
      "aurelia-dialog",
      "components/confirm-dialog",
      "lib/ws-client",
      "aurelia-event-aggregator"
    ],
    "pages/ebooks.js": [
      "aurelia-framework",
      "lib/api-client"
    ],
    "pages/login.js": [
      "lib/access",
      "aurelia-framework"
    ],
    "pages/search.js": [
      "aurelia-framework",
      "lib/api-client"
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
    "test/test-page.js": [
      "aurelia-framework",
      "lib/api-client"
    ]
  }
});