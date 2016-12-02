
export class PidiCache {
  constructor(duration) {
    this._cache = new Map();
    this.duration = duration*1000;
  }

  add(entityName, entity) {
    this._cache.set(entityName, {ts: new Date(), entity})
  }

  get(entityName, entityId) {
    if (this._cache.has(entityName) && this._cache.get(entityName).entity.id == entityId) {
      let rec = this._cache.get(entityName)
      if (new Date() - rec.ts <= this.duration) return rec.entity
      else this._cache.delete(entityName)
    }
  }

  clear(entityName) {
    this._cache.delete(entityName);
  }
}
