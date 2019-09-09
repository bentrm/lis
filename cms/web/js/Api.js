import $ from 'jquery';
import {currentLanguage} from './lang';


const filter = (obj) =>
  Object.keys(obj)
    .filter(key => obj[key])
    .reduce((res, key) => (res[key] = obj[key], res), {});


export default class Api {
  constructor(rootUrl) {
    this.rootUrl = rootUrl;
  }

  getResults(path, options = {}) {
    const params = filter(options);
    const queryParams = `?${$.param(params, true)}`;
    const url = `${this.rootUrl}${path}${queryParams}`;
    return fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Accept-Language': currentLanguage,
      }
    }).then(response => response.json());
  }

  getAuthors(options) {
    return this.getResults('/authors', options);
  }

  getAuthor(id, options) {
    return this.getResults(`/authors/${id}`, options);
  }

  getPositions(options) {
    return this.getResults('/positions', options);
  }

  getMemorials(options) {
    return this.getResults('/memorials', options);
  }

  getMemorial(id) {
    return this.getResults(`/memorials/${id}`);
  }
}
