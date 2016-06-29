import {LogManager, inject} from 'aurelia-framework';
import {Configure} from  'lib/config/index'

let logger=LogManager.getLogger('notifications');
const MAX_SIZE=20;

@inject(Configure)
export class Notification {
  _dirty = false;
  _ns=[];
  _details=new Map()

  constructor(config) {
    if (config.get('debug')) {
      this._ns=['aaaaa'];
      this._details.set('aaaaa',{text:'Extra metadata from file xxxx',
            'type': 'metadata',
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
    } else {
      logger.warn(`Update for uknown task ${taskId}`);
    }

  }

  get items() {
    let a = [];
    for (let taskId of this._ns) {
      a.push(this._details.get(taskId));
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
