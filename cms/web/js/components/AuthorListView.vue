<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div class="row align-items-stretch">
    <main class="col m-4">
      <div class="row">
        <div class="col-12">
          <h3>{{ 'Authors' | translate }} ({{ count }})</h3>
        </div>
        <div class="col-12">
          <pagination
            class="align-content-center"
            :currentPage="page"
            :totalPages="totalPages"
            v-on:change="setPage"></pagination>
        </div>
        <div
          v-for="author in authors"
          :key="author.id"
          class="col-12"
        >
          <author-card
            :image="author.title_image"
            :url="author.url"
            :academic_title="author.academic_title"
            :first_name="author.first_name"
            :last_name="author.last_name"
            :birth_name="author.birth_name"></author-card>
        </div>
        <div class="col-12">
          <pagination
            class="align-content-center"
            :currentPage="page"
            :totalPages="totalPages"
            v-on:change="setPage"></pagination>
        </div>
      </div>
    </main>
    <aside class="Sidebar col-6 col-lg-4 border-bottom border-sm-bottom-0 border-sm-left order-first order-sm-last pt-2">
      <h5>{{ 'Keyword search..' | translate }}</h5>
      <filter-list
        v-on:change="onGenreFilterChange"
        :items="genreFilterList"
        :selection="genreSelection">
        <template v-slot:header>{{ genreFilterHeader }}</template>
      </filter-list>

      <filter-list
        v-on:change="onLanguageFilterChange"
        :items="languageFilterList"
        :selection="languageSelection">
        <template v-slot:header>{{ languageFilterHeader }}</template>
      </filter-list>

      <filter-list
        v-on:change="onPeriodFilterChange"
        :items="periodFilterList"
        :selection="periodSelection">
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
</template>

<script>
  import AuthorCard from './AuthorCard.vue';
  import Pagination from './Pagination.vue';
  import FilterList from './FilterList.vue';
  import FilterItem from './FilterItem.vue';
  import api from '../Api';
  import translate from '../translate';


  export default {

    components: {
      AuthorCard,
      Pagination,
      FilterList,
      FilterItem,
    },

    filters: {
      translate,
    },

    data () {
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
          {title: translate('Female'), id: 'F'},
          {title: translate('Male'), id: 'M'}
        ],
        genderSelection: new Set()
      };
    },
    computed: {

      offset () {
        const vm = this;
        return (vm.page - 1) * vm.limit;
      },

      totalPages: function () {
        const vm = this;
        return Math.ceil(vm.count / vm.limit);
      },

      authorParams () {
        const vm = this;
        return {
          genre: [...vm.genreSelection],
          language: [...vm.languageSelection],
          period: [...vm.periodSelection],
          gender: [...vm.genderSelection],
          ordering: 'last_name',
          limit: vm.limit,
          offset: vm.offset,
        };
      },

      tagParams () {
        return {
          ordering: 'name',
          limit: 1000,
        };
      },

      genreFilterHeader () {
        const vm = this;
        return `${translate('Genres')} (${vm.genreSelection.size} / ${vm.genres.length})`;
      },

      genreFilterList () {
        return this.genres.map(x => ({
          id: x.id,
          title: `${x.name}`,
        }));
      },

      languageFilterHeader () {
        const vm = this;
        return `${translate('Languages')} (${vm.languageSelection.size} / ${vm.languages.length})`;
      },

      languageFilterList () {
        return this.languages.map(x => ({
          id: x.id,
          title: `${x.name}`,
        }));
      },

      periodFilterHeader () {
        const vm = this;
        return `${translate('Periods')} (${vm.periodSelection.size} / ${vm.periods.length})`;
      },

      periodFilterList () {
        return this.periods.map(x => ({
          id: x.id,
          title: `${x.name}`,
        }));
      }
    },

    watch: {
      authorParams () {
        const vm = this;
        vm.fetchAuthors();
      },
    },

    created: function () {
      const vm = this;
      vm.fetchGenres();
      vm.fetchLanguages();
      vm.fetchPeriods();
      vm.fetchAuthors();
    },

    methods: {

      fetchAuthors: function () {
        const vm = this;
        api
          .getAuthors(vm.authorParams)
          .then(json => {
            vm.count = json.count;
            vm.authors = json.results;
          });
      },

      fetchGenres () {
        const vm = this;
        api
          .getResults('/genres', vm.tagParams)
          .then(json => vm.genres = json.results);
      },

      fetchLanguages () {
        const vm = this;
        api
          .getResults('/languages', vm.tagParams)
          .then(json => vm.languages = json.results);
      },

      fetchPeriods () {
        const vm = this;
        api
          .getResults('/periods', vm.tagParams)
          .then(json => vm.periods = json.results);
      },

      onGenreFilterChange (selection) {
        const vm = this;
        vm.setPage(1);
        vm.genreSelection = selection;
      },

      onLanguageFilterChange (selection) {
        const vm = this;
        vm.setPage(1);
        vm.languageSelection = selection;
      },

      onPeriodFilterChange (selection) {
        const vm = this;
        vm.setPage(1);
        vm.periodSelection = selection;
      },

      onGenderFilterChange (selection) {
        const vm = this;
        vm.setPage(1);
        vm.genderSelection = selection;
      },

      setPage: function (pageNumber) {
        this.page = pageNumber;
      }
    }
  };
</script>
