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
        <FilterList
          :title="'Authors'"
          :items="authors"
          :selection="authorSelection"
          v-on:change="onAuthorSelectionChange"></FilterList>
        <FilterList
          :title="'Memorial types'"
          :items="types"
          :selection="typeSelection"
          v-on:change="onTypeSelectionChange"></FilterList>
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

      authorFilters () {
        return {
          ordering: 'last_name',
          limit: 1000,
        };
      },

      memorialFilters () {
        return {
          author: [...this.authorSelection],
          memorial_type: [...this.typeSelection],
          limit: 1000,
        };
      },

      typeFilters () {
        return {
          ordering: 'title',
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

      onAuthorSelectionChange (selection) {
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
