<template>
  <div class="container-fluid">
    <div class="row">
      <main class="col m-4">
        <div class="row">
          <div class="offset-3 offset-md-2 offset-lg-1 col-9 col-md-10 col-lg-11">
            <h3>{{ 'Authors' | translate }} ({{ count }})</h3>
          </div>
          <div class="offset-3 offset-md-2 offset-lg-1 col-9 col-md-10 col-lg-11">
            <pagination
              class="align-content-center"
              :currentPage="page"
              :totalPages="totalPages"
              v-on:change="setPage"
            ></pagination>
          </div>
          <ul class="col-12">
            <li v-for="author in authors" :key="author.id" class="row h4 pb-1">
              <div class="col-3 col-md-2 col-lg-1 justify-content-center align-content-center">
                <cms-image
                  v-if="author.title_image"
                  :src="author.title_image.thumb"
                  :alt="author.title_image.title"
                  :title="author.title_image.title"
                  class="border border-primary rounded-circle img-fluid"
                ></cms-image>
              </div>

              <div class="col">
                <router-link :to="{name: 'author-detail', params: { slug: author.slug }}">
                  <span v-if="author.first_name" class="small text-muted">{{ author.first_name }}</span>
                  {{ author.last_name }}
                </router-link>
              </div>
            </li>
          </ul>
          <div class="offset-3 offset-md-2 offset-lg-1 col-9 col-md-10 col-lg-11">
            <pagination
              class="align-content-center"
              :currentPage="page"
              :totalPages="totalPages"
              v-on:change="setPage"
            ></pagination>
          </div>
        </div>
      </main>
      <aside
        class="Sidebar col-6 col-lg-4 border-bottom border-sm-bottom-0 border-sm-left order-first order-sm-last pt-2"
      >
        <h5>{{ 'Keyword search' | translate }}</h5>
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
      </aside>
    </div>
  </div>
</template>

<script>
import api from '../Api';
import translate from '../translate';
import CmsImage from './CmsImage.vue';
import FilterItem from './FilterItem.vue';
import FilterList from './FilterList.vue';
import Pagination from './Pagination.vue';

export default {
  components: {
    CmsImage,
    Pagination,
    FilterList,
    FilterItem
  },

  filters: {
    translate
  },

  data() {
    return {
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

  methods: {
    fetchAuthors: function() {
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

    setPage: function(pageNumber) {
      this.page = pageNumber;
    }
  }
};
</script>
