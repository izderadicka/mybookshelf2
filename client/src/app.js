import { FetchConfig, AuthorizeStep} from 'aurelia-auth';
import {inject,LogManager,bindable} from 'aurelia-framework';
import { HttpClient} from 'aurelia-fetch-client';
import {Configure} from 'lib/config/index';
import {WSClient} from 'lib/ws-client';
import {Access} from 'lib/access';
import {ROUTES} from 'routes';
import {ConfirmDialog} from 'components/confirm-dialog';
import {DialogService} from 'aurelia-dialog';
import {EventAggregator} from 'aurelia-event-aggregator';

const logger = LogManager.getLogger('app');
@inject(Configure, FetchConfig, HttpClient, WSClient, Access, DialogService, EventAggregator)
export class App {
  constructor(config, fetchConfig, client, wsClient, access, dialog, event) {
    this.config = config;
    this.access=access;
    this.dialog=dialog;
    event.subscribe('user-session-expired', () => this.showExpiredDialog());
    fetchConfig.configure();
    client.configure(conf => conf
      .withBaseUrl(`${this.config.get('api.protocol',window.location.protocol)}//${this.config.get('api.host',window.location.hostname)}:${this.config.get('api.port', window.location.port)}`)

      .withInterceptor({
        response: response => {
          if (response && response.status == 401) {
            logger.warn('Not authenticated!');
            this.access.redirectToLogin();
            throw new Error('Not autherticated!');

          } else if (response && response.status >= 300)
            throw new Error(`HTTP error ${response.status}`);
          return response;
        }
      })
    );

  }

  showExpiredDialog() {
    this.dialog.open({
        viewModel: ConfirmDialog,
        model: {
          action: 'Renew session',
          message: `Session with server has expired. Do you want to renew it?`
        }
      })
      .then(resp => {
        if (!resp.wasCancelled) {
          let redir = (err) => {
            logger.warn(`Cannot refresh session: ${err}`);
            this.access.redirectToLogin();
          }
          this.access.refreshLogin().
          then(() => {
            if (this.access.authenticated) {
              logger.debug('Session refreshed')
            }
            else {
              redir();
            }
            })
          .catch((err) => redir(JSON.stringify(err)));

        }
      });
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

  get authenticated() {
    return this.access.authenticated;
  }

  authenticatedChanged() {
    logger.debug('Authenticated changed!')
  }

  doSearch(query) {
    this.router.navigateToRoute('search', {
      query: encodeURIComponent(query)
    });
  }
}
