<template>
  <div class="container-fluid">
    <div class="row">
      <main v-if="!isSmallDevice" class="col p-4">
        <div class="row">
          <div class="col-12">
            <h3>{{ 'Authors' | translate }} ({{ count }})</h3>

            <author-list
              :authors="authors"
              :page="page"
              :count="count"
              :totalPages="totalPages"
              v-on:change="setPage" />
          </div>
        </div>
      </main>

      <b-card class="Sidebar col col-sm-6 col-lg-4 p-0" no-body>
        <b-tabs card pills small fill>
          <b-tab v-if="isSmallDevice" :active="$route.name === 'author-list'">
            <template v-slot:title>
              <i class="fas fa-book"></i>
              {{ 'Authors' | translate }} ({{ count }})
            </template>
            <author-list
              :authors="authors"
              :page="page"
              :count="count"
              :totalPages="totalPages"
              v-on:change="setPage" />
          </b-tab>

          <b-tab>
            <template v-slot:title>
              <i class="fas fa-search"></i>
              {{ 'Filters' | translate }}
            </template>
            <filter-list
              v-on:change="onGenreFilterChange"
              :items="genreFilterList"
              :selection="genreSelection"
            >
              <template v-slot:header>{{ genreFilterHeader }}</template>
            </filter-list>

            <filter-list
              v-on:change="onLanguageFilterChange"
              :items="languageFilterList"
              :selection="languageSelection"
            >
              <template v-slot:header>{{ languageFilterHeader }}</template>
            </filter-list>

            <filter-list
              v-on:change="onPeriodFilterChange"
              :items="periodFilterList"
              :selection="periodSelection"
            >
              <template v-slot:header>{{ periodFilterHeader }}</template>
            </filter-list>

            <filter-list
              v-on:change="onGenderFilterChange"
              :items="genders"
              :selection="genderSelection"
              :searchable="false"
              :collapsable="false"
            >
              <template v-slot:header>{{ 'Gender' | translate }}</template>
            </filter-list>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
  import api from '../Api';
  import translate from '../translate';
  import FilterList from '../components/FilterList.vue';
  import {getDeviceWidth} from '../utils';
  import AuthorList from '../components/AuthorList.vue';

  export default {
  components: {
    AuthorList,
    FilterList,
  },

  filters: {
    translate
  },

  metaInfo: {
    title: translate('Authors'),
  },

  data() {
    return {
      isSmallDevice: getDeviceWidth() < 576,

      page: 1,
      limit: 20,
      authors: [],
      count: 0,

      genres: [],
      genreSelection: new Set(),

      languages: [],
      languageSelection: new Set(),

      periods: [],
      periodSelection: new Set(),

      genders: [
        { title: translate('Female'), id: 'F' },
        { title: translate('Male'), id: 'M' }
      ],
      genderSelection: new Set()
    };
  },
  computed: {
    offset() {
      const vm = this;
      return (vm.page - 1) * vm.limit;
    },

    totalPages: function() {
      const vm = this;
      return Math.ceil(vm.count / vm.limit);
    },

    authorParams() {
      const vm = this;
      return {
        genre: [...vm.genreSelection],
        language: [...vm.languageSelection],
        period: [...vm.periodSelection],
        gender: [...vm.genderSelection],
        ordering: 'last_name',
        limit: vm.limit,
        offset: vm.offset
      };
    },

    tagParams() {
      return {
        ordering: 'name',
        limit: 1000
      };
    },

    genreFilterHeader() {
      const vm = this;
      return `${translate('Genres')} (${vm.genreSelection.size} / ${
        vm.genres.length
      })`;
    },

    genreFilterList() {
      return this.genres.map(x => ({
        id: x.id,
        title: `${x.name}`
      }));
    },

    languageFilterHeader() {
      const vm = this;
      return `${translate('Languages')} (${vm.languageSelection.size} / ${
        vm.languages.length
      })`;
    },

    languageFilterList() {
      return this.languages.map(x => ({
        id: x.id,
        title: `${x.name}`
      }));
    },

    periodFilterHeader() {
      const vm = this;
      return `${translate('Periods')} (${vm.periodSelection.size} / ${
        vm.periods.length
      })`;
    },

    periodFilterList() {
      return this.periods.map(x => ({
        id: x.id,
        title: `${x.name}`
      }));
    }
  },

  watch: {
    authorParams() {
      const vm = this;
      vm.fetchAuthors();
    }
  },

  created: function() {
    const vm = this;
    vm.fetchGenres();
    vm.fetchLanguages();
    vm.fetchPeriods();
    vm.fetchAuthors();
  },

  mounted() {
    window.onresize = this.onWindowResize;
  },

  methods: {
    onWindowResize() {
      this.isSmallDevice = getDeviceWidth() < 576;
    },

    fetchAuthors() {
      const vm = this;
      api.getAuthors(vm.authorParams).then(json => {
        vm.count = json.count;
        vm.authors = json.results;
      });
    },

    fetchGenres() {
      const vm = this;
      api
        .getResults('/genres', vm.tagParams)
        .then(json => (vm.genres = json.results));
    },

    fetchLanguages() {
      const vm = this;
      api
        .getResults('/languages', vm.tagParams)
        .then(json => (vm.languages = json.results));
    },

    fetchPeriods() {
      const vm = this;
      api
        .getResults('/periods', vm.tagParams)
        .then(json => (vm.periods = json.results));
    },

    onGenreFilterChange(selection) {
      const vm = this;
      vm.setPage(1);
      vm.genreSelection = selection;
    },

    onLanguageFilterChange(selection) {
      const vm = this;
      vm.setPage(1);
      vm.languageSelection = selection;
    },

    onPeriodFilterChange(selection) {
      const vm = this;
      vm.setPage(1);
      vm.periodSelection = selection;
    },

    onGenderFilterChange(selection) {
      const vm = this;
      vm.setPage(1);
      vm.genderSelection = selection;
    },

    setPage(pageNumber) {
      this.page = pageNumber;
    }
  }
};
</script>

<style lang="scss">
  @import 'src/scss/variables';

  .author-thumb {
    max-height: 25px;
  }
</style>
