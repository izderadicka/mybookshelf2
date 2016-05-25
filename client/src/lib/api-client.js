import {HttpClient, json} from 'aurelia-fetch-client';
import {inject} from 'aurelia-framework';
import $ from 'bootstrap';
import {Configure} from 'lib/config/index';

@inject(Configure, HttpClient)
export class ApiClient {
  constructor(config, http) {
    this.http=http;
    this.apiPath=config.get('api.path');
    this.baseUrl=http.baseUrl;
  }

  getUrl(r, query=null) {
    return this.apiPath+'/'+r+(query?'?'+$.param(query):'');
  }

  post(resource, data) {
    return this.http.fetch(this.getUrl(resource),
    {method:'post',
    body:json(data)

    })
    .then(resp => resp.json())
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

  getOne(resource, id) {
    const url=this.getUrl(resource+'/'+ id)
    return this.http.fetch(url)
      .then(response => response.json());
  }

  checkUpload(fileInfo) {
    return this.post('upload/check', fileInfo)
      .then(data => {
        if (data.error) throw new Error(data.error);
      });
  }
}
