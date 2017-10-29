import {Notification} from 'lib/notification';
import {Access} from 'lib/access';
import {inject,LogManager} from 'aurelia-framework';
import {Configure} from 'lib/config/index';
import {EventAggregator} from 'aurelia-event-aggregator';
import {AsexorClient, WampAsexorClient, LongPollAsexorClient} from 'izderadicka/asexor_js_client';

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
  constructor(config, notif, event, access) {
    this.notif = notif;
    this.access = access;
    this.config = config;

    event.subscribe('user-logged-in', (evt) => this.connect(evt.user));
    event.subscribe('user-logged-out', () => this.disconnect());
    event.subscribe('user-session-expired', () => this.disconnect());

  }

  connect(userEmail) {
    if (! this.access.authenticated) throw new Error('Not Authenticated');
    if (this.conn) {
      logger.warn('Connection already exists');
      this.conn.close();
    }
    let wsHost = `${this.config.get('backend-ws.host', location.hostname)}:${this.config.get('backend-ws.port', location.port)}`;
    this.conn = new AsexorClient(wsHost, this.access.token);
    logger.debug('WS connection requested');
    this.conn.connect()
      .then( () => this.onConnectionOpen())
      .catch((err) => this.onConnectionClose(err));
  }

  get isConnected() {
    return (this.conn !== null && this.conn.active);
  }

  disconnect() {
    if (this.conn) {
      this.conn.close();
      logger.debug('Disconnected WS connection');
      this.conn = null;
      
    }
  }

  onConnectionOpen() {
    logger.debug('WS connection opened');
    this.conn.subscribe((taskId, data) => {
    logger.debug(`Notification for task ${taskId} with data ${JSON.stringify(data)}`);
    this.notif.update(taskId, data);
    });

  }

  onConnectionClose(reason, details) {
    if (!details || details.reason !== 'wamp.close.normal')
      logger.warn(`WAMP connection closed ${reason} : ${JSON.stringify(details)}`);
    this.conn=null;
  }

  @connected
  extractMeta(fileName, originalFileName=null, proposedMeta={}) {
    return this.conn.exec('metadata', [fileName, proposedMeta])
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
    return this.conn.exec('convert',  [source.id, format])
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
    return this.conn.exec('convert-many', [entityName, entity.id, format])
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
    return this.conn.exec('cover', [uploadedCover, ebook.id])
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
