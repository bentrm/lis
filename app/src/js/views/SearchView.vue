<template>
  <page-layout class="mb-5">
    <div class="row p-4">
      <div class="col-12">
        <h3>{{ 'Search' | translate }}</h3>
        <search-bar class="mb-2" v-on:submit="fetchQueryResults" v-on:change="fetchQueryResults"></search-bar>
      </div>

      <div class="col-12 col-md-6" v-if="memorials.length">
        <h3 class="text-muted">{{ memorialsHeading }}</h3>

        <ul class="list-unstyled">
          <list-row
            v-for="memorial in memorials"
            :key="memorial.id"
            :imgThumb="memorial.title_image && memorial.title_image.thumb"
            :imgTitle="memorial.title_image && memorial.title_image.title"
            :to="{name: 'map-detail', params: { memorialId: memorial.id }}"
          >
            {{ memorial.name }}
          </list-row>
        </ul>
      </div>

      <div class="col-12 col-md-6" v-if="authors.length">
        <h3 class="text-muted">{{ authorsHeading }}</h3>

        <ul class="list-unstyled">
          <author-list-row v-for="author in authors" :key="author.id" :author="author"/>
        </ul>
      </div>

      <div class="col-12" v-if="!memorials.length && !authors.length">
        <div v-if="!firstSearch" class="alert alert-primary my-4" role="alert">
          <span >{{ 'No results..' | translate }}</span>
        </div>
        <div v-else class="alert alert-dark my-4" role="alert">
          <span >{{ 'Please enter a search term..' | translate }}</span>
        </div>
      </div>
    </div>
  </page-layout>
</template>

<script>
  import translate from '../translate';
  import api from '../Api';
  import PageLayout from '../components/PageLayout.vue';
  import CmsImage from '../components/CmsImage.vue';
  import ListRow from '../components/ListRow.vue';
  import AuthorListRow from '../components/AuthorListRow.vue';
  import SearchBar from '../components/SearchBar.vue';

  export default {

    components: {
      AuthorListRow,
      CmsImage,
      ListRow,
      SearchBar,
      PageLayout,
    },

    filters: {
      translate
    },

    data() {
      const vm = this;
      const query = vm.$route.query.q || '';

      return {
        firstSearch: true,
        limit: 20,
        query,
        authors: [],
        authorsCount: 0,
        memorials: [],
        memorialsCount: 0
      };
    },

    computed: {
      memorialsHeading() {
        return `${translate('Memorials')}`;
      },
      authorsHeading() {
        return `${translate('Authors')}`;
      }
    },

    mounted() {
      this.fetchQueryResults(this.query);
    },

    methods: {
      resetResults() {
        const vm = this;

        vm.firstSearch = true;
        vm.memorials = [];
        vm.memorialsCount = 0;
        vm.authors = [];
        vm.authorsCount = 0;
      },

      async fetchQueryResults(query) {
        const vm = this;
        const options = { search: query, limit: vm.limit };

        if (query.length < 1) {
          vm.resetResults();
          return;
        } else {
          vm.firstSearch = false;
        }

        vm.fetchMemorials(options);
        vm.fetchAuthors(options);
      },

      async fetchMemorials(options) {
        const vm = this;
        const response = await api.getMemorials(options);
        vm.memorials = response.results;
        vm.memorialsCount = response.count;
      },

      async fetchAuthors(options) {
        const vm = this;
        const response = await api.getAuthors(options);
        vm.authors = response.results;
        vm.authorsCount = response.count;
      }
    },

    watch: {
      query: function(newQuery, oldQuery) {
        const vm = this;
        if (newQuery.length < 1) {
          vm.resetResults();
        } else {
          vm.fetchQueryResults(newQuery);
        }
      }
    }

  }
</script>

<style lang="scss">

</style>
