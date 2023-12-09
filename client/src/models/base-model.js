import {BindingEngine, LogManager} from 'aurelia-framework';
import {Container} from 'aurelia-dependency-injection';

const logger = LogManager.getLogger('base-model');

export class BaseModel {
  constructor(obj, editableProperties) {
    this.editableProperties = editableProperties;
    let bindingEngine = Container.instance.get(BindingEngine);
    if (obj) Object.assign(this, obj);

    this._disposers=[];
    this._changed = new Set();

    let bind = (prop, asArray) => {
      let observer;
      let obj = this;
      let parts=prop.split('.');
      let propName=parts[0];

      while (parts.length >1) {
        let disp =  bindingEngine.propertyObserver(obj, parts[0])
          .subscribe((n,o) => this.changed(propName));
        this._disposers.push(disp);
        let newObj = obj[parts[0]];
        if (!newObj) {
          newObj = {};
          obj[parts[0]] = newObj;
        }
        obj = newObj;
        prop = parts[1];
        parts.shift();
      }

      if (asArray) {
        if (!obj[prop]) obj[prop] = [];
        observer = bindingEngine.collectionObserver(obj[prop]);
      } else {
        observer=bindingEngine.propertyObserver(obj, prop);
      }
      let disp = observer.subscribe((n,o) => this.changed(propName,n,o));
      this._disposers.push(disp);
    }

    for (let [prop, asArray] of this.editablePropsFullNames)
      bind(prop, asArray);
  }

  get dirty() {
    return this._changed.size > 0;
  }

  get editableProps() {
    return this.editableProperties.map(p => {
      p = p.split('.')[0];
      return p.endsWith('[]')? p.slice(0,-2):p;
    })
  }

  get editablePropsFullNames() {
    return this.editableProperties.map(p => {
      return p.endsWith('[]')? [p.slice(0,-2), true]:[p, false];
    })
  }

  isNew() {
    return ! this.id ;
  }

  changed(prop, n, o) {
    logger.debug('Property changed '+prop);
    this._changed.add(prop);
  }

  hasChanged(prop) {
    return this._changed && this._changed.has(prop)
  }

  dispose() {
    this._disposers.forEach(d => d.dispose());
  }

  validate(addError) {
    throw new Error('Must be overriden in child class');
  }

  prepareData() {
    let data = {}

    let normNull = function(x) {
      if (x === '') return null;
      return x;
    }

    let shrink = function(obj) {
      if  (!obj) return null;
      if (obj.hasOwnProperty('id') && obj.id) {
        return {id:obj.id}
      } else {
        let newObj = {}
        for (let prop of Object.keys(obj)) {
          if (prop !=='id' && obj[prop]) newObj[prop] = obj[prop]
        }
        if (Object.keys(newObj).length === 0) return null;
        return newObj;
      }
    };

      let shrinkList = function(l) {
        if (!l) return [];
        return l.map(shrink).filter(x => x);
      }

      let compareObjects = function(o1, o2) {
        return JSON.stringify(o1) === JSON.stringify(o2);
      }

    for (let prop of this.editableProps) {
      if (this.isNew() || this._changed.has(prop)) {
        let val = this[prop];
        if (Array.isArray(val))
          val = shrinkList(val);
        else if (typeof val === 'object')
          val = shrink(val)
        data[prop] = normNull(val);
      }
    }

    if (! this.isNew() && Object.keys(data).length) {
      data.id = this.id;
      data.version_id = this.version_id;
    }

    logger.debug(`New data : ${JSON.stringify(data)}`);
    return data;

  }


}
