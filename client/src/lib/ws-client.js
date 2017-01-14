import {Notification} from 'lib/notification';
import {Access} from 'lib/access';
import {inject,LogManager} from 'aurelia-framework';
import {Configure} from 'lib/config/index';
import {EventAggregator} from 'aurelia-event-aggregator';

import autobahn from 'mins/autobahn.min';

const logger = LogManager.getLogger('ws-client');

function connected(target, prop, descriptor) {
  let fn = descriptor.value;
  let wrapped = function() {
    if (! this.isConnected) {
      alert('WebSocket is not connected, reload application!');
      return Promise.reject(new Error('Websocket is not connected'));
    } else {
      return fn.apply(this,arguments)
    }
  }
  descriptor.value = wrapped;
  return descriptor;
}

@inject(Configure, Notification, EventAggregator, Access)
export class WSClient {
  conn = null;
  session = null;
  constructor(config, notif, event, access) {
    this.notif = notif;
    this.access = access;
    this.config = config;

    window.AUTOBAHN_DEBUG = true;

    event.subscribe('user-logged-in', (evt) => this.connect(evt.user));
    event.subscribe('user-logged-out', () => this.disconnect());

  }

  connect(userEmail) {
    if (! this.access.authenticated) throw new Error('Not Authenticated');
    if (this.conn) {
      logger.warn('Connection already exists');
      this.conn.close();
    }
    let connUrl = `${location.protocol ==='https:'?'wss:':'ws:'}//${this.config.get('wamp.host', location.hostname)}:${this.config.get('wamp.port')}${this.config.get('wamp.path')}`;
    this.conn = new autobahn.Connection({
      url: connUrl,
      realm: this.config.get('wamp.realm'),
      authmethods: ["ticket"],
      authid: userEmail,
      onchallenge: (session, method, extra) => this.onChallenge(session, method, extra)
    });
    logger.debug('WAMP connection requested');
    this.conn.onopen = (session, details) => this.onConnectionOpen(session, details);
    this.conn.onclose = this.onConnectionClose;
    this.conn.open();
  }

  get isConnected() {
    return (this.session !== null)
  }

  disconnect() {
    if (this.conn) {
      this.conn.close();
      logger.debug('Disconnected WS connection');
      this.conn = null;
      this.session = null;
    }
  }

  receiveNotification(args, kwargs, options) {
    logger.debug(`Notification ${JSON.stringify(args)}, ${JSON.stringify(kwargs)}`);
    this.notif.update(args[0], kwargs);
  }

  onChallenge(session, method, extra) {
    logger.debug(`Authentication required, method ${method}`);
    if (method === 'ticket') {
      return this.access.token;
    } else {
      throw new Error('invalid auth method');
    }

  }

  onConnectionOpen(session, details) {
    logger.debug('WAMP connection opened : ' + JSON.stringify(details));
    this.session = session
    session.subscribe('eu.zderadicka.asexor.task_update', (args, kwargs, options) =>
        this.receiveNotification(args, kwargs, options))
      .then(sub => logger.debug('WAMP subscribed to notifications'),
        err => logger.error('WAMP Failed to subscribe to notifications ' + JSON.stringify(err)));

  }

  onConnectionClose(reason, details) {
    logger.warn(`WAMP connection closed ${reason} : ${JSON.stringify(details)}`);
    this.conn=null;
    this.session=null;
  }

  @connected
  extractMeta(fileName, originalFileName=null, proposedMeta={}) {
    return this.session.call('eu.zderadicka.asexor.run_task', ['metadata',fileName, proposedMeta])
    .then(taskId => {
      this.notif.start(taskId,
        {
        text:`Extract metadata from ${originalFileName || fileName}`,
        status:"submitted",
        task:"metadata",
        taskId,
        file: fileName,
        originalFileName
      });
      return taskId;
    });
  }

  @connected
  convertSource(source, format, ebook) {
    return this.session.call('eu.zderadicka.asexor.run_task', ['convert', source.id, format])
      .then(taskId => {
        this.notif.start(taskId,
          {
          text:`Convert ebook ${ebook.title}: from ${source.format} to ${format}`,
          status:"submitted",
          task:"convert",
          taskId,
          sourceId: source.id,
          ebookId: ebook.id
        });
        return taskId;
      })
  }

  @connected
  convertMany(entityName, entity, format) {
    return this.session.call('eu.zderadicka.asexor.run_task', ['convert-many', entityName, entity.id, format])
      .then(taskId => {
        this.notif.start(taskId,
          {
          text:`Convert all ebooks for ${entityName} ${entity.last_name || entity.title || entity.name} to ${format}`,
          status:"submitted",
          task:"convert-many",
          taskId,
          entityId: entity.id,
          entityName: entityName
        });
        return taskId;
      })
  }

  @connected
  changeCover(uploadedCover, ebook) {
    return this.session.call('eu.zderadicka.asexor.run_task', ['cover', uploadedCover, ebook.id])
    .then(taskId => {
      this.notif.start(taskId,
        {
        text:`Update ebook ${ebook.title} cover image.`,
        status:"submitted",
        task:"cover",
        taskId,
        ebookId: ebook.id
      });
      return taskId;
    })
  }

}
