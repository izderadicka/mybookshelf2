export class App {
  configureRouter(config, router) {
    config.title = 'MyBookshelf2';
    config.map([
      { route: ['', 'welcome'], name: 'welcome',      moduleId: 'pages/welcome', nav: true, title: 'Welcome' },
      {route: 'ebooks', name:'ebooks',  moduleId: 'pages/ebooks', nav:true, title:'Ebooks'},
      { route: 'ebook/:id', name:'ebook', moduleId: 'pages/ebook', title:'Ebook'}
      /*
      { route: 'users',         name: 'users',        moduleId: 'pages/users',        nav: true, title: 'Github Users' },
      { route: 'child-router',  name: 'child-router', moduleId: 'pages/child-router', nav: true, title: 'Child Router' } */
    ]);

    this.router = router;
  }
}
