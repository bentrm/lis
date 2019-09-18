<template>
  <div class="row">
    <main class="col-xs-12 col-sm mt-4">
      <div class="row">
        <div class="col-12">
          <h3>Authors ({{ count }})</h3>
        </div>
        <div class="col-12">
          <Pagination
            :currentPage="currentPage"
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
            :currentPage="currentPage"
            :totalPages="totalPages"
            v-on:change="setPage"></Pagination>
        </div>
      </div>
    </main>
    <aside
      id="Filterbar"
      class="Filterbar col-sm-5 col-md-3 col-lg-2 border-bottom border-sm-bottom-0 border-sm-left order-first order-sm-last mb-2"
    >
      <form name="filter-form" class="p-2">
        <TagFilter
          v-for="filter in tagFilters"
          :key="filter.id"
          :api="api"
          :id="filter.id"
          :label="filter.label"
          :param="filter.param"
          :path="filter.path"
          v-on:change="onFilterChange"></TagFilter>
        <RadioFilter
          :id="genderFilter.id"
          :label="genderFilter.label"
          :param="genderFilter.param"
          :options="genderFilter.options"
          v-on:change="onFilterChange"></RadioFilter>
      </form>
    </aside>
  </div>
</template>

<script>
  import AuthorCard from './AuthorCard.vue';
  import Pagination from './Pagination.vue';
  import RadioFilter from './RadioFilter.vue';
  import TagFilter from './TagFilter.vue';


  export default {
    props: ['api'],
    components: {
      AuthorCard,
      Pagination,
      RadioFilter,
      TagFilter,
    },
    data: function () {
      return {
        filters: {
          ordering: 'last_name',
          limit: 20,
          offset: 0,
        },
        count: 0,
        authors: [],
        tagFilters: [
          {
            id: 'genre',
            label: 'Genre',
            param: 'genre',
            path: '/genres',
          },
          {
            id: 'language',
            label: 'Languages',
            param: 'language',
            path: '/languages',
          },
          {
            id: 'period',
            label: 'Period',
            param: 'period',
            path: '/periods'
          }
        ],
        genderFilter: {
          id: 'gender',
          label: 'Gender',
          param: 'gender',
          options: [
            {label: 'All', value: '', checked: true},
            {label: 'Female', value: 'F', checked: false},
            {label: 'Male', value: 'M', checked: false},
          ]
        },
      };
    },
    computed: {
      currentPage: function () {
        const vm = this;
        return vm.filters.offset / vm.limit;
      },
      totalPages: function () {
        const vm = this;
        return Math.ceil(vm.count / vm.filters.limit);
      }
    },
    created: function () {
      const vm = this;
      vm.fetchAuthors();
    },
    methods: {
      setPage: function (pageNumber) {
        const vm = this;
        const newOffset = (pageNumber - 1) * vm.filters.limit;
        vm.setFilterParam('offset', newOffset);
      },
      setFilterParam: function (param, value) {
        const vm = this;
        if (param !== 'offset') {
          vm.filters['offset'] = 0;
        }
        vm.filters[param] = value;
        vm.fetchAuthors();
      },
      fetchAuthors: function () {
        const vm = this;
        vm.api
          .getAuthors(vm.filters)
          .then(json => {
            vm.count = json.count;
            vm.authors = json.results;
          });
      },
      onFilterChange: function (param, value) {
        const vm = this;
        vm.setFilterParam(param, value);
      }
    }
  };
</script>
