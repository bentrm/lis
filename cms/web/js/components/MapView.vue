<template>
  <div class="row h-100">

    <main class="col p-0">
      <Map
        :initialView="initialView"
        :memorials="memorials"
        v-on:click="selectMemorial"
        v-on:moveend="onMapMoveEnd"></Map>
    </main>

    <aside class="col-6 col-lg-4 h-100 overflow-auto border-left">
      <router-view
        :api="api"
        v-on:hideMemorialDetail="unselectMemorial"></router-view>
    </aside>
  </div>
</template>

<script>
  import {getMapView, mapCenterToPath, setMapView} from '../utils';
  import Map from './Map.vue';
  import api from '../Api';

  function data() {
    return {
      api,
      filters: {
        limit: 1000,
      },
      initialView: {
        center: [50.7, 14.9],
        zoom: 8,
      },
      memorial: null,
      memorials: [],
    };
  }

  function mounted() {
    const vm = this;
    vm.fetchMemorials();

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
    const mapState = mapCenterToPath(center, zoom);

    if (vm.historyAction) {
      vm.historyAction = false;
      return;
    }

    this.$router.push({name: this.$route.name, params: { mapState }});
  }

  function fetchMemorials() {
    const vm = this;
    vm.api
      .getMemorials(vm.filters)
      .then(json => vm.memorials = json.results);
  }

  function selectMemorial(id) {
    const vm = this;
    vm.$router.push({name: 'memorial-detail', params: { ...this.$route.params, id}});
  }

  function unselectMemorial() {
    const vm = this;
    vm.memorial = null;
  }

  function setFilterParam(param, value) {
    const vm = this;
    vm.filters[param] = value;
    vm.fetchMemorials();
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
    components: {
      Map,
    },
    data,
    mounted,
    methods: {
      onMapMoveEnd,
      fetchMemorials,
      setFilterParam,
      selectMemorial,
      unselectMemorial,
      onAuthorChange,
      onFilterChange,
      onPopState
    }
  };
</script>
