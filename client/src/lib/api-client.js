import {HttpClient} from 'aurelia-fetch-client';
import {inject} from 'aurelia-framework';
import 'fetch';
import {ApplicationState} from 'lib/application-state';

@inject(HttpClient, ApplicationState)
export class ApiClient {
  constructor(http,state) {
    http.configure(config => {
      config
        .withBaseUrl(`http://${window.location.hostname}:6006`)
        //.withDefaults({headers:{'Authorization': state.token}})
        });
    this.http=http;
    this.state=state;
  }

  getMany(resource, page=1, pageSize=25, sort, extra='') {
    const url='/'+resource+`?page=${page}&max_results=${pageSize}` +
      (sort?`&sort=${sort}`:'')+extra;
    return this.http.fetch(url)
      .then(response => response.json())
      .then(data => {let lastPage=Math.ceil(data._meta.total / pageSize);
                    return {data:data._items, lastPage:lastPage}})
  }

  search(query, page=1, pageSize=25) {
    return this.getMany('search', page, pageSize, null,
    `&where={"$text":{"$search":"${encodeURIComponent(query)}"}}&projection={"score":{"$meta":"textScore"}}&sort=[("score",{"$meta": "textScore"})]` )
  }

  authorBooks(lastname, firstname, filter=null, page=1, pageSize=34, sort) {
    lastname=encodeURIComponent(lastname);
    firstname=firstname?encodeURIComponent(firstname):null;
    filter = filter?`, "title": {"$regex":"${encodeURIComponent(filter)}", "$options":"i"}`:'';
    return this.getMany('ebooks', page, pageSize, sort,
  `&where={"authors.lastname": "${lastname}", "authors.firstname":${firstname?`"${firstname}"`:'null'}${filter}}`);
  }

  getOne(resource, id) {
    const url='/'+resource+'/'+id;
    return this.http.fetch(url)
      .then(response => response.json());
  }
}
