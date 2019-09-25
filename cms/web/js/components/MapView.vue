<template>
  <div class="row h-100">

    <main class="col p-0">
      <Map
        :initial-map-state="initialMapState"
        :features="memorials"
        v-on:select="onMapSelect"
        v-on:moveend="onMapMoveEnd"></Map>
    </main>

    <aside class="col-6 col-lg-4 h-100 overflow-auto border-left">

      <div class="p-2" v-if="$route.name === 'map'">

        <h4>{{memorials.length}} memorials found:</h4>

        <filter-list
          v-on:change="onAuthorFilterChange"
          :items="authors"
          :selection="authorSelection">
          <template v-slot:header>{{ authorFiltersHeader }}</template>
          <template v-slot:item="{item}">
            {{item.last_name}}, {{item.first_name}}
          </template>
        </filter-list>

        <filter-list
          v-on:change="onTypeSelectionChange"
          :items="types"
          :selection="typeSelection">
          <template v-slot:header>{{ typeFiltersHeader }}</template>
          <template v-slot:item="{item}">
            {{item.name}}
          </template>
        </filter-list>
      </div>

      <router-view
        :memorial="memorialSelect"
        v-on:hide="onMemorialDetailHide"></router-view>
    </aside>
  </div>
</template>

<script>
  import {mapStateToPath, pathToMapState} from '../utils';
  import Map from './Map.vue';
  import FilterList from './FilterList.vue';
  import api from '../Api';

  export default {
    props: {
      mapStatePath: {
        type: String,
        default: '@13.4,51.8,7z',
      },
      memorialId: [String, Number],
    },

    components: {
      Map,
      FilterList,
    },

    data() {
      return {
        initialMapState: undefined,
        manualRouteTransition: false,

        memorials: [],
        memorialSelect: undefined,

        // authors
        authors: [],
        authorSelection: new Set(),

        // types
        types: [],
        typeSelection: new Set(),
      };
    },

    computed: {

      authorFiltersHeader () {
        const vm = this;
        return `Authors (${vm.authorSelection.size} / ${vm.authors.length})`;
      },

      typeFiltersHeader () {
        const vm = this;
        return `Types (${vm.typeSelection.size} / ${vm.types.length})`;
      },

      authorFilters () {
        return {
          ordering: 'last_name,first_name',
          limit: 1000,
        };
      },

      memorialFilters () {
        return {
          author: [...this.authorSelection],
          memorial_type: [...this.typeSelection],
          ordering: 'name',
          limit: 1000,
        };
      },

      typeFilters () {
        return {
          ordering: 'name',
          limit: 1000,
        };
      }

    },

    watch: {
      mapStatePath (newMapStatePath) {
        const vm = this;
        if (vm.manualRouteTransition) {
          vm.initialMapState = pathToMapState(newMapStatePath);
        }
      },

      memorialId (newMemorialId) {
        const vm = this;
        if (newMemorialId) {
          vm.fetchMemorial();
        } else {
          vm.memorialSelect = null;
        }
      },

      memorialFilters (newFilters) {
        this.fetchMemorials();
      }
    },

    created() {
      const vm = this;

      vm.initialMapState = pathToMapState(vm.mapStatePath);
      vm.fetchMemorials();
      vm.fetchAuthors();
      vm.fetchTypes();

      if (vm.memorialId) {
        vm.fetchMemorial();
      }

      // bind back/forward button to event handler
      window.onpopstate = vm.onPopState;
    },

    methods: {

      onMapSelect(memorialId) {
        const vm = this;

        if (memorialId) {
          vm.$router
            .push({
              name: 'memorial-detail',
              params: { ...vm.$route.params, memorialId }
            })
            .catch(() => {});
        } else {
          vm.$router
            .push({
              name: 'map',
              params: { ...vm.$route.params }
            })
            .catch(() => {});
        }
      },

      onMapMoveEnd(center, zoom) {
        const vm = this;
        const mapStatePath = mapStateToPath(center, zoom);

        if (vm.manualRouteTransition) {
          vm.manualRouteTransition = false;
          return;
        }

        vm.$router.push({name: vm.$route.name, params: { ...vm.$route.params, mapStatePath }});
      },

      onPopState () {
        this.manualRouteTransition = true;
      },

      onAuthorFilterChange (selection) {
        this.authorSelection = selection;
      },

      onTypeSelectionChange (selection) {
        this.typeSelection = selection;
      },

      onMemorialDetailHide () {
        const vm = this;
        vm.$router
          .push({
            name: 'map',
            params: { ...vm.$route.params }
          })
          .catch(() => {});
      },

      fetchMemorials() {
        const vm = this;
        api
          .getMemorials(vm.memorialFilters)
          .then(json => vm.memorials = json.results);
      },

      fetchMemorial() {
        const vm = this;
        api
          .getMemorial(vm.memorialId)
          .then(json => vm.memorialSelect = json);
      },

      fetchAuthors() {
        const vm = this;
        api
          .getAuthors(vm.authorFilters)
          .then(json => {
            const results = json.results;
            results.forEach(x => x.title = `${x.first_name} ${x.last_name}`);
            vm.authors = results;
          });
      },

      fetchTypes() {
        const vm = this;
        api
          .getResults('/memorialTypes', vm.typeFilters)
          .then(json => vm.types = json.results);
      }
    }
  };
</script>
