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
      this._details.set('aaaaa',{text:'Converted ebook TEST ',
            'task': 'convert',
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
      let data = this._details.get(taskId);
      Object.assign(data, obj);
      this._dirty = true;
      logger.debug(`Task updated ${taskId}`);
      let task = data.task;
      if (task) {
        if (obj.status === 'success') this.event.publish(`${task}-ready`, {taskId, result: obj.result, data});
        else if (obj.status === 'error') this.event.publish(`${task}-error`, {taskId, error: obj.error, data});
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
