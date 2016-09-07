import {LogManager, inject} from 'aurelia-framework';
import {Configure} from  'lib/config/index'
import {EventAggregator} from 'aurelia-event-aggregator';

let logger=LogManager.getLogger('notifications');
const MAX_SIZE=20;

@inject(Configure, EventAggregator)
export class Notification {

  constructor(config, event) {
    this.event = event;
    this._observers = new Set();
    this._ns=[];
    this._details=new Map()
    /*
    if (config.get('debug')) {
      this._ns=['aaaaa'];
      this._details.set('aaaaa',{text:'Converted ebook TEST ',
            'task': 'convert',
            'start': new Date(),
            'status':'success',
            'result': 3});
    }
    */
  }

  addObserver(o) {
    this._observers.add(o)
    return () => this._observers.delete(0);
    }

  updateObservers(action, status) {
    this._observers.forEach(o => o(action, status));
  }

  start(taskId, taskInfo) {

    this._ns.unshift(taskId);
    taskInfo.start=new Date();
    this._details.set(taskId, taskInfo);
    if (this._ns.length > MAX_SIZE) {
      let k = this._ns.pop();
      this._details.delete(k);
    }
    this.updateObservers('start');
  }

  update(taskId, obj) {
    if (this._details.has(taskId)) {
      let data = this._details.get(taskId);
      Object.assign(data, obj);
      this.updateObservers('update', obj.status);
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

  get empty() {
    return ! this._ns || this._ns.length === 0
  }

}
