<template>
  <div class="row">
    <main class="col m-4">
      <div class="row">
        <div class="col-12">
          <h3>Authors ({{ count }})</h3>
        </div>
        <div class="col-12">
          <Pagination
            :currentPage="page"
            :totalPages="totalPages"
            v-on:change="setPage"></Pagination>
        </div>
        <div
          v-for="author in authors"
          :key="author.id"
          class="col-12"
        >
          <AuthorCard
            :thumb="author.thumb"
            :url="author.url"
            :academic_title="author.academic_title"
            :first_name="author.first_name"
            :last_name="author.last_name"
            :birth_name="author.birth_name"></AuthorCard>
        </div>
        <div class="col-12">
          <Pagination
            :currentPage="page"
            :totalPages="totalPages"
            v-on:change="setPage"></Pagination>
        </div>
      </div>
    </main>
    <aside
      id="Filterbar"
      class="Filterbar col-6 col-lg-4 border-bottom border-sm-bottom-0 border-sm-left order-first order-sm-last mb-2"
    >
      <form name="filter-form" class="p-2">
        <filter-list
          v-on:change="onGenreFilterChange"
          :items="genres"
          :selection="genreSelection">
          <template v-slot:header>{{ genreFiltersHeader }}</template>
          <template v-slot:item="{item}">
            {{item.name}}
          </template>
        </filter-list>

        <filter-list
          v-on:change="onLanguageFilterChange"
          :items="languages"
          :selection="languageSelection">
          <template v-slot:header>{{ languageFiltersHeader }}</template>
          <template v-slot:item="{item}">
            {{item.name}}
          </template>
        </filter-list>

        <filter-list
          v-on:change="onPeriodFilterChange"
          :items="periods"
          :selection="periodSelection">
          <template v-slot:header>{{ periodFiltersHeader }}</template>
          <template v-slot:item="{item}">
            {{item.name}}
          </template>
        </filter-list>

        <filter-list
          v-on:change="onGenderFilterChange"
          :items="genders"
          :selection="genderSelection">
          <template v-slot:header>Gender</template>
          <template v-slot:item="{item}">
            {{item.name}}
          </template>
        </filter-list>
      </form>
    </aside>
  </div>
</template>

<script>
  import AuthorCard from './AuthorCard.vue';
  import Pagination from './Pagination.vue';
  import FilterList from './FilterList.vue';
  import FilterItem from './FilterItem.vue';
  import api from '../Api';


  export default {

    components: {
      AuthorCard,
      Pagination,
      FilterList,
      FilterItem,
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
          {name: 'Female', id: 'F'},
          {name: 'Male', id: 'M'}
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

      genreFiltersHeader () {
        const vm = this;
        return `Genres (${vm.genreSelection.size} / ${vm.genres.length})`;
      },

      languageFiltersHeader () {
        const vm = this;
        return `Languages (${vm.languageSelection.size} / ${vm.languages.length})`;
      },

      periodFiltersHeader () {
        const vm = this;
        return `Periods (${vm.periodSelection.size} / ${vm.periods.length})`;
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
