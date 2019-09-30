<template>
  <form class="form-inline d-flex search-bar">
    <div class="flex-grow-1 ml-lg-4 mr-lg-2">
      <input
        v-model="query"
        class="form-control w-100"
        type="search"
        :placeholder="'Search' | translate"
        aria-label="Search"
      >
      <ul
        class="list-unstyled ml-lg-4 search-bar-results"
        v-if="memorials.length || authors.length"
      >
        <li class="text-muted text-monospace" v-if="memorials.length">
          <u>{{ memorialsHeading }}</u>
        </li>
        <li v-for="result in memorials">
          <a :href="`/map/@${result.position[0]},${result.position[1]},18z/memorial/${result.id}`" :alt="result.name">
          {{ result.name }}
          </a>
        </li>
        <li class="text-muted text-monospace" v-if="authors.length">
          <u>{{ authorsHeading }}</u>
        </li>
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
</template>

<script>
  import api from '../Api';
  import translate from '../translate';

  export default {
    name: 'search-bar',
    filters: {
      translate,
    },
    data: function () {
      return {
        limit: 5,
        query: '',
        authors: [],
        authorsCount: 0,
        memorials: [],
        memorialsCount: 0,
      };
    },
    computed: {
      memorialsHeading () {
        return `${translate('Memorials')} (${this.memorials.length} / ${this.memorialsCount})`;
      },
      authorsHeading () {
        return `${translate('Authors')} (${this.authors.length} / ${this.authorsCount})`;
      }
    },
    methods: {
      fetchQueryResults: function (query) {
        const vm = this;
        const options = {search: query, limit: vm.limit};

        api
          .getMemorials(options)
          .then(json => {
            vm.memorials = json.results;
            vm.memorialsCount = json.count;
          });
        api
          .getAuthors(options)
          .then(json => {
            vm.authors = json.results;
            vm.authorsCount = json.count;
          });
      }
    },
    watch: {
      query: function (newQuery, oldQuery) {
        const vm = this;
        vm.fetchQueryResults(newQuery);
      }
    }
  };

</script>

<style lang="scss">
  @import "../../scss/variables";

  .search-bar {
    position: relative;

    .search-bar-results {
      display: none;
      font-size: .8rem;
      position: absolute;
      left: 0;
      right: 0;
      background-color: white;
      border: $input-border-width solid $input-border-color;
      padding: $input-padding-x $input-padding-y;
      z-index: 1000;

      li {
        margin-bottom: .2rem;
      }
    }
  }

  .search-bar:focus-within {
    .search-bar-results {
      display: block;
    }
  }
</style>
