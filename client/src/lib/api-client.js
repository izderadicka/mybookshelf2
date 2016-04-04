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
        .withBaseUrl(`http://${window.location.hostname}:5000/`)
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

  getMany(resource, page=1, pageSize=25, sort) {
    const url=resource+`?page=${page}&max_results=${pageSize}` +
      (sort?`&sort=${sort}`:'');
    return this.http.fetch(url, {headers:{'Authorization': this.state.token}})
      .then(response => response.json())
      .then(data => {let lastPage=Math.ceil(data._meta.total / pageSize);
                    return {data:data._items, lastPage:lastPage}})
  }

  getOne(resource, id) {
    const url=resource+'/'+id;
    return this.http.fetch(url, {headers:{'Authorization': this.state.token}})
      .then(response => response.json());
  }
}
