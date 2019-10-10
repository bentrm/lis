import queryString from 'query-string';
import {currentLanguage} from './translate';


const filter = (obj) =>
  Object.keys(obj)
    .filter(key => obj[key])
    .reduce((res, key) => {
      res[key] = obj[key];
      return res;
    }, {});

class Api {
  constructor(rootUrl) {
    this.rootUrl = rootUrl;
  }

  getResults(path, options = {}) {
    const params = filter(options);
    const queryParams = queryString.stringify(params);
    const url = `${this.rootUrl}${path}?${queryParams}`;
    return fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Accept-Language': currentLanguage(),
      }
    }).then(response => {
      if (response.status !== 200) {
        throw response;
      }
      return response.json()
    });
  }

  getPage(slug, options) {
    return this.getResults(`/page/${slug}`, options);
  }

  getAuthors(options) {
    return this.getResults('/authors', options);
  }

  getAuthor(slug, options) {
    return this.getResults(`/authors/${slug}`, options);
  }

  getLevel(slug, level, options) {
    return this.getResults(`/authors/${slug}/${level}`, options);
  }

  getMemorials(options) {
    return this.getResults('/memorials', options);
  }

  async getMemorial(id) {
    return this.getResults(`/memorials/${id}`);
  }
}

export default new Api('/api/v2');
