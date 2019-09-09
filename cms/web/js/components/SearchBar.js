import Vue from 'vue/dist/vue.esm';
import Api from '../Api';

const api = new Api('/api/v2');

const template = `
  <form class="form-inline d-flex search-bar">
    <div class="flex-grow-1 ml-lg-4 mr-lg-2">
      <input 
        v-model="query"
        class="form-control w-100" 
        type="search" 
        placeholder="Search..." 
        aria-label="Search"        
       >
      <ul 
        class="list-unstyled search-bar-results" 
        v-if="memorials.length || authors.length"
      >
        <li class="display-4" v-if="memorials.length">Memorials</li>
        <li v-for="result in memorials">
          {{ result.title }}
        </li>
        <li class="display-4" v-if="authors.length">Authors</li>
        <li v-for="result in authors">
          <a :href="result.url">
            {{ result.first_name }} {{ result.last_name }}
          </a>          
        </li>
      </ul>
    </div>    
    <button class="btn btn-outline-light my-2 my-sm-0" type="submit">
      <i class="fas fa-search"></i>
    </button>
  </form>
`;

Vue.component('search-bar', {
  template,
  data: function() {
    return {
      query: '',
      authors: [],
      memorials: [],
    };
  },
  methods: {
    fetchQueryResults: function(query) {
      const vm = this;
      const options = { search: query, limit: 5 };

      api
        .getMemorials(options)
        .then(json => vm.memorials = json.results);
      api
        .getAuthors(options)
        .then(json => vm.authors = json.results);
    }
  },
  watch: {
    query: function(newQuery, oldQuery) {
      const vm = this;
      vm.fetchQueryResults(newQuery);
    }
  }
});
