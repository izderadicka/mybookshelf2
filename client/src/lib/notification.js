import {LogManager, inject} from 'aurelia-framework';
import {Configure} from  'lib/config/index'
import {EventAggregator} from 'aurelia-event-aggregator';

let logger=LogManager.getLogger('notifications');
const MAX_SIZE=20;

@inject(Configure, EventAggregator)
export class Notification {
  _dirty = false;
  _ns=[];
  _details=new Map()

  constructor(config, event) {
    this.event = event;
    if (config.get('debug')) {
      this._ns=['aaaaa'];
      this._details.set('aaaaa',{text:'Extra metadata from file xxxx',
            'task': 'metadata',
            'start': new Date(),
            'status':'success',
            'result': 3});
    }
  }
  start(taskId, taskInfo) {

    this._ns.unshift(taskId);
    taskInfo.start=new Date();
    this._details.set(taskId, taskInfo);
    if (this._ns.length > MAX_SIZE) {
      let k = this._ns.pop();
      this._details.delete(k);
    }
    this._dirty=true;
  }

  update(taskId, obj) {
    if (this._details.has(taskId)) {
      Object.assign(this._details.get(taskId), obj);
      this._dirty = true;
      logger.debug(`Task updated ${taskId}`);
      if (this._details.get(taskId).task === 'metadata') {
        if (obj.status === 'success') this.event.publish('metadata-ready', {taskId, result: obj.result});
        else if (obj.status === 'error') this.event.publish('metadata-error', {taskId, error: obj.error});
      }

    } else {
      logger.warn(`Update for uknown task ${taskId}`);
    }

  }

  markDone(taskId) {
    if (this._details.has(taskId)) {
      this._details.get(taskId).done = true;
    }
  }

  get items() {
    let a = [];
    for (let taskId of this._ns) {
      let notif = this._details.get(taskId);
      a.push(notif);
    }
    return a;
  }

  get dirty() {
    return this._dirty;
  }

  resetDirty() {
    this._dirty=false;
  }



}
