import {EventAggregator} from 'aurelia-event-aggregator';
import {Notification} from 'lib/notification';
import {
  inject,
  LogManager}
from 'aurelia-framework';
import {
  Configure
} from 'lib/config/index';

import autobahn from 'autobahn.min';

const logger = LogManager.getLogger('ws-client');

@inject(Configure, Notification, EventAggregator)
export class WSClient {
  conn=null
  session=null
  constructor(config, notif, event) {
    this.notif=notif
    this.event=event
    let connUrl=`ws://${config.get('wamp.host')}:${config.get('wamp.port')}${config.get('wamp.path')}`;
    this.conn=new autobahn.Connection({url:connUrl,realm:config.get('wamp.realm')});
    logger.debug('WAMP connection requested');
    this.conn.onopen=(session, details) => this.onConnectionOpen(session, details);
    this.conn.onclose=this.onConnectionClose;
    this.conn.open();
  }

  receiveNotification(args, kwargs, options) {
    //logger.debug('Notification '+args);
    this.event.publish('notifications', {args, kwargs});
    this.notif.add({text:'Notification', args, kwargs});
  }

  onConnectionOpen(session, details) {
    logger.debug('WAMP connection opened');
    this.session=session
    session.subscribe('eu.zderadicka.mybookshelf2.heartbeat', (args, kwargs, options) =>
            this.receiveNotification(args, kwargs, options))
    .then(sub => logger.debug('WAMP subscribed to notifications'),
          err => logger.error('WAMP Failed to subscribe to notifications '+err));

  }

  onConnectionClose(reason, details) {
    logger.warn(`WAMP connection closed ${reason}`);
  }

}
