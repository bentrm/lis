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
        v-show="memorials.length || authors.length"
      >
        <li class="text-muted text-monospace" v-if="memorials.length">
          <u>{{ memorialsHeading }}</u>
        </li>
        <li v-for="result in memorials">
          <router-link
            :to="{name: 'memorial-detail', params: { mapStatePath: `@${result.position[0]},${result.position[1]},18z`, memorialId: result.id }}"
            :alt="result.name">
            {{ result.name }}
          </router-link>
        </li>
        <li class="text-muted text-monospace" v-if="authors.length">
          <u>{{ authorsHeading }}</u>
        </li>
        <li v-for="result in authors">
          <router-link
            :to="{name: 'author-detail', params: { slug: result.slug }}"
            :alt="result.name">
            {{ result.first_name }} {{ result.last_name }}
          </router-link>
        </li>
      </ul>
    </div>
    <button
      class="btn btn-outline-light my-2 my-sm-0"
      :disabled="query.length < 3"
      type="button"
      v-on:click="fetchQueryResults"
    >
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
      resetResults () {
        const vm = this;

        vm.memorials = [];
        vm.memorialsCount = 0;
        vm.authors = [];
        vm.authorsCount = 0;
      },

      fetchQueryResults: function (query) {
        const vm = this;
        const options = {search: query, limit: vm.limit};

        if (query.length < 3) {
          vm.resetResults();
          return;
        }

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
      z-index: 1010;

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
