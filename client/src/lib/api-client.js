import {HttpClient, json} from 'aurelia-fetch-client';
import {inject} from 'aurelia-framework';
import $ from 'bootstrap';
import {Configure} from 'lib/config/index';
import {PidiCache} from './pidi-cache';

@inject(Configure, HttpClient)
export class ApiClient {
  constructor(config, http) {
    this.http=http;
    this.apiPath=config.get('api.path');
    this.baseUrl=http.baseUrl;
    this._cache = new Map();
    this._cache2 = new PidiCache(60);
  }

  getUrl(r, query=null) {
    return this.apiPath+'/'+r+(query?'?'+$.param(query):'');
  }

  post(resource, data) {
    return this.http.fetch(this.getUrl(resource),
    {method:'POST',
      body:json(data)
    })
    .then(resp => resp.json())
  }

  delete(resource, id) {
    return this.http.fetch(this.getUrl(resource)+'/'+id,
      {method:'DELETE'})
    .then(resp => resp.json());
  }

  patch(resource, data, id) {
    return this.http.fetch(this.getUrl(resource+'/'+id),
    {method: 'PATCH',
    body:json(data)})
    .then(resp => resp.json());
  }

  getIndex(resource, start) {
    let url = this.getUrl(resource + '/index/' + encodeURIComponent(start));
    return this.http.fetch(url).then(response => response.json());
  }

  getManyUnpagedCached(resource) {
    let now = new Date();
    if (this._cache.has(resource) && (now - this._cache.get(resource).ts) < 60*3600*1000) {
      return Promise.resolve(this._cache.get(resource).data)
    }
    let url = this.getUrl(resource);
    return this.http.fetch(url)
      .then(response => response.json())
      .then(data => {
        this._cache.set(resource, {ts: new Date(), data});
        return data
      });
  }

  getManyUnpaged(resource) {
    let url = this.getUrl(resource);
    return this.http.fetch(url)
      .then(response => response.json());
  }

  getMany(resource, page=1, pageSize=25, sort, extra) {
    let query={page:page, page_size:pageSize,sort:sort};
    if (extra) {
      for (let k in extra)
        if (extra.hasOwnProperty(k)) query[k]=extra[k];
    }
    const url=this.getUrl(resource, query);
    return this.http.fetch(url)
      .then(response => response.json())
      .then(data => {let lastPage=Math.ceil(data.total / data.page_size);
                    return {data:data.items, lastPage:lastPage}})
  }

  search(query, page=1, pageSize=25) {
    return this.getMany('search/'+encodeURIComponent(query), page, pageSize)
  }

  authorBooks(id, filter=null, page=1, pageSize=34, sort) {
    return this.getMany('ebooks/author/'+id, page, pageSize, sort, filter?{filter:encodeURIComponent(filter)}:null);
  }

  getOne(resource, id, fresh) {
    if (!fresh) {
      let cached = this._cache2.get(resource, id);
      if (cached) return Promise.resolve(cached);
    }
    let url=this.getUrl(resource+'/'+ id)
    return this.http.fetch(url)
      .then(response => response.json())
      .then(entity => {
        this._cache2.add(resource, entity);
        return entity;
      });
  }

  clearCache(resource) {
    this._cache2.clear(resource);
  }

  checkUpload(fileInfo) {
    return this.post('upload/check', fileInfo)
      .then(data => {
        if (data.error) throw new Error(data.error);
      });
  }

  upload(formData, resource='upload') {
    return this.http.fetch(this.getUrl(resource), {method:'post', body: formData})
      .then( resp => resp.json())
  }


  addUploadToEbook(ebookId, uploadId, quality) {
    return this.post(`ebooks/${ebookId}/add-upload`, {upload_id:uploadId, quality});
  }

  merge(resource, entityId, otherId) {
    return this.post(`${resource}/${entityId}/merge`, {other_ebook: otherId});
  }

  getCover(resource, id) {
    let url =  this.getUrl(resource+'/'+id+'/cover')
    return this.http.fetch(url)
    .then(r => r.blob())
  }
}
