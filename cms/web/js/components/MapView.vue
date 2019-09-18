<template>
  <div class="row h-100">

    <main class="col p-0">
      <Map
        :initialView="initialView"
        :positions="positions"
        v-on:click="showMemorial"
        v-on:moveend="onMapMoveEnd"></Map>
    </main>

    <aside class="col-6 col-lg-4 h-100 overflow-auto border-left">

      <div v-if="memorial">
        <span v-on:click="onUnselect"><i class="fas fa-times-circle"></i></span>
        <h3>{{memorial.title}}</h3>
        <img
          v-if="memorial.thumb"
          :src="memorial.thumb"
          :alt="memorial.title"
          class="Memorial-badge border border-primary rounded-circle align-self-center">
        <ul class="list-unstyled">
          <li v-for="author in memorial.authors" v-if="author" :key="author.id">
            <a :href="author.url">{{author.first_name}} {{author.last_name}}</a>
          </li>
        </ul>
        <div v-html="memorial.address"></div>
        <div v-html="memorial.contact_info"></div>
        <div v-html="memorial.directions"></div>
        <div v-html="memorial.introduction"></div>
      </div>

      <form v-else name="filter-form" class="p-2">
        <AuthorFilter
          id="author-filter"
          :api="api"
          v-on:change="onAuthorChange"
        ></AuthorFilter>
        <TagFilter
          v-for="(filter, index) in tagFilters"
          :key="index"
          :api="api"
          :id="filter.id"
          :label="filter.label"
          :param="filter.param"
          :path="filter.path"
          v-on:change="onFilterChange"></TagFilter>
      </form>
    </aside>
  </div>
</template>

<script>
  import {getMapView, setMapView} from '../utils';
  import AuthorFilter from './AuthorFilter.vue';
  import Map from './Map.vue';
  import TagFilter from './TagFilter.vue';


  function data() {
    return {
      filters: {
        limit: 1000,
      },
      initialView: {
        center: [50.7, 14.9],
        zoom: 8,
      },
      memorial: null,
      positions: [],
      tagFilters: [
        {
          id: 'memorialType',
          label: 'Memorial type',
          param: 'memorial_type',
          path: '/memorialTypes',
        },
      ],
    };
  }

  function mounted() {
    const vm = this;
    vm.fetchPositions();

    window.onpopstate = vm.onPopState;
  }

  function onPopState() {
    const vm = this;
    const newInitialView = getMapView(window.location.href);

    if (newInitialView) {
      vm.historyAction = true;
      vm.initialView = newInitialView;
    }
  }

  function onMapMoveEnd(center, zoom) {
    const vm = this;
    const newHref = setMapView(window.location.href, {center, zoom});

    if (vm.historyAction) {
      vm.historyAction = false;
      return;
    }

    window.history.pushState({center, zoom}, document.title, newHref);
  }

  function fetchPositions() {
    const vm = this;
    vm.api
      .getPositions(vm.filters)
      .then(json => vm.positions = json.results);
  }

  function showMemorial(id) {
    const vm = this;
    vm.api
      .getMemorial(id)
      .then(json => vm.memorial = json);
  }

  function onUnselect() {
    const vm = this;
    vm.memorial = null;
  }

  function setFilterParam(param, value) {
    const vm = this;
    vm.filters[param] = value;
    vm.fetchPositions();
  }

  function onAuthorChange(author) {
    const vm = this;
    vm.setFilterParam('author', author);
  }

  function onFilterChange(param, value) {
    const vm = this;
    vm.setFilterParam(param, value);
  }

  export default {
    name: 'map-view',
    props: ['api'],
    components: {
      AuthorFilter,
      Map,
      TagFilter,
    },
    data,
    mounted,
    methods: {
      onMapMoveEnd,
      fetchPositions,
      setFilterParam,
      showMemorial,
      onUnselect,
      onAuthorChange,
      onFilterChange,
      onPopState
    }
  };
</script>
