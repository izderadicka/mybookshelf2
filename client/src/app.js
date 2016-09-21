import { FetchConfig, AuthorizeStep} from 'aurelia-auth';
import {inject,LogManager,bindable} from 'aurelia-framework';
import { HttpClient} from 'aurelia-fetch-client';
import {Configure} from 'lib/config/index';
import {WSClient} from 'lib/ws-client';
import {Access} from 'lib/access';
import {ROUTES} from 'routes';

const logger = LogManager.getLogger('app');
@inject(Configure, FetchConfig, HttpClient, WSClient, Access)
export class App {
  constructor(config, fetchConfig, client, wsClient, access) {
    this.config = config;
    this.access=access;
    fetchConfig.configure();
    client.configure(conf => conf
      .withBaseUrl(`http://${this.config.get('api.host',window.location.hostname)}:${this.config.get('api.port', window.location.port)}`)

      .withInterceptor({
        response: response => {
          if (response && response.status == 401) {
            logger.warn('Not authenticated!');
            this.router.navigateToRoute('login');
            throw new Error('Not autherticated!');

          } else if (response && response.status >= 300)
            throw new Error(`HTTP error ${response.status}`);
          return response;
        }
      })
    );

  }

  configureRouter(config, router) {
    config.title = 'MyBookshelf2';
    config.addPipelineStep('authorize', AuthorizeStep);
    config.map(ROUTES);

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
