
const MAX_SIZE=20;

export class Notification {
  _dirty = false;
  _ns=[];

  add(n) {
    this._ns.unshift(n);
    if (this._ns.length > MAX_SIZE) this._ns.pop();
    this._dirty=true;
  }

  get items() {
    return this._ns;
  }

  get dirty() {
    return this._dirty;
  }

  resetDirty() {
    this._dirty=false;
  }



}
