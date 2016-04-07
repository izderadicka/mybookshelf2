export class App {
  configureRouter(config, router) {
    config.title = 'Login to MyBookshelf2';
    config.map([
      {route: ['login', ''], name: 'login', moduleId:'pages/login', title:'Login'},
    ]);

    this.router = router;
  }
}
