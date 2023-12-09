import {inject, LogManager, computedFrom, bindable} from 'aurelia-framework';

export class Conversions {

  configureRouter(config, router) {
    this.router = router;
    config.map([
      {route: '', redirect: 'batch-conversions'},
      {route: 'batch-conversions', name:'batch-conversions', moduleId: 'pages/batch-conversions',
       title: 'Batch Conversions', nav: 1, auth: true},
      {route: 'ebook-conversions', name:'ebook-conversions', moduleId: 'pages/ebook-conversions',
       title: 'Ebooks Conversions', nav: 2, auth: true}
    ])
  }
}
