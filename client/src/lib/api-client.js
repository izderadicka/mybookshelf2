import {HttpClient} from 'aurelia-fetch-client';
import {inject} from 'aurelia-framework';
import 'fetch';
import {ApplicationState} from 'lib/application-state';

@inject(HttpClient, ApplicationState)
export class ApiClient {
  constructor(http,state) {
    http.configure(config => {
      config
        .useStandardConfiguration()
        .withBaseUrl(`http://${window.location.hostname}:6006/`)
        .withDefaults({
          credentials: 'same-origin',
          headers: {
            'Accept': 'application/json'
          }
          })
        });
    this.http=http;
    this.state=state;
  }

  getMany(resource, page=1, pageSize=25, sort, extra='') {
    const url=resource+`?page=${page}&max_results=${pageSize}` +
      (sort?`&sort=${sort}`:'')+extra;
    return this.http.fetch(url, {headers:{'Authorization': this.state.token}})
      .then(response => response.json())
      .then(data => {let lastPage=Math.ceil(data._meta.total / pageSize);
                    return {data:data._items, lastPage:lastPage}})
  }

  search(query, page=1, pageSize=25) {
    return this.getMany('search', page, pageSize, null,
    `&where={"$text":{"$search":"${encodeURIComponent(query)}"}}&projection={"score":{"$meta":"textScore"}}&sort=[("score",{"$meta": "textScore"})]` )
  }

  authorBooks(lastname, firstname, page=1, pageSize=34, sort) {
    lastname=encodeURIComponent(lastname);
    firstname=firstname?encodeURIComponent(firstname):null;
    return this.getMany('ebooks', page, pageSize, sort,
  `&where={"authors.lastname": "${lastname}", "authors.firstname":${firstname?`"${firstname}"`:'null'}}`);
  }

  getOne(resource, id) {
    const url=resource+'/'+id;
    return this.http.fetch(url, {headers:{'Authorization': this.state.token}})
      .then(response => response.json());
  }
}
