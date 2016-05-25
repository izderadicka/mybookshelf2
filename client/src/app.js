import { FetchConfig, AuthorizeStep} from 'aurelia-auth';
import {inject,LogManager,bindable} from 'aurelia-framework';
import { HttpClient} from 'aurelia-fetch-client';
import {Configure} from 'lib/config/index';
import {Notification} from 'lib/notification';
import {WSClient} from 'lib/ws-client';
import {Access} from 'lib/access';

const logger = LogManager.getLogger('app');
@inject(Configure, FetchConfig, HttpClient, WSClient, Notification, Access)
export class App {
  constructor(config, fetchConfig, client, wsClient, notif, access) {
    this.config = config;
    this.notif=notif;
    this.access=access;
    fetchConfig.configure();
    client.configure(conf => conf
      .withBaseUrl(`http://${this.config.get('api.hostname',window.location.hostname)}:${this.config.get('api.port')}`)

      .withInterceptor({
        response: response => {
          if (response && response.status == 401) {
            logger.warn('Not authenticated!');
            this.router.navigateToRoute('login');
            throw new Error('Not autherticated!');

          }
          return response;
        }
      })
    );

  }

  configureRouter(config, router) {
    config.title = 'MyBookshelf2';
    config.addPipelineStep('authorize', AuthorizeStep);
    config.map([{
        route: ['', 'welcome'],
        name: 'welcome',
        moduleId: 'pages/welcome',
        nav: true,
        title: 'Welcome'
      }, {
        route: 'ebooks',
        name: 'ebooks',
        moduleId: 'pages/ebooks',
        nav: true,
        title: 'Ebooks',
        auth: true
      }, {
        route: 'login',
        name: 'login',
        moduleId: 'pages/login',
        title: 'Login'
      }, {
        route: 'ebook/:id',
        name: 'ebook',
        moduleId: 'pages/ebook',
        title: 'Ebook',
        auth: true
      }, {
        route: 'search/:query',
        name: 'search',
        moduleId: 'pages/search',
        title: 'Search Results',
        auth: true
      }, {
        route: ['author/:id'],
        name: 'author',
        moduleId: 'pages/author',
        title: 'Authors books',
        auth: true
      }
      
    ]);

    this.router = router;
  }

  activate() {
    this.access.signalState();
  }

  isAuthenticated() {
    return this.access.authenticated;
  }

  doSearch(query) {
    this.router.navigateToRoute('search', {
      query: encodeURIComponent(query)
    });
  }
}
