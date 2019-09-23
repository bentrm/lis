<template>
  <div class="row h-100">

    <main class="col p-0">
      <Map
        :initialView="initialView"
        :memorial="memorial"
        :memorials="memorials"
        v-on:click="selectMemorial"
        v-on:moveend="onMapMoveEnd"></Map>
    </main>

    <aside class="col-6 col-lg-4 h-100 overflow-auto border-left">
      <router-view
        :api="api"
        :memorial="memorial"
        v-on:hideMemorialDetail="selectMemorial(null)"></router-view>
    </aside>
  </div>
</template>

<script>
  import {mapCenterToPath, pathToMapCenter} from '../utils';
  import Map from './Map.vue';
  import api from '../Api';

  export default {
    props: {
      mapState: {
        type: String,
        default: '@14.9,50.7,8z'
      }
    },

    components: {
      Map,
    },

    data() {
      return {
        api,

        initialView: {
          center: [50.7, 14.9],
          zoom: 8,
        },

        // memorial details
        memorial: null,
        memorialError: null,
        memorialLoading: false,

        // memorials
        memorials: [],
        memorialFilters: {
          limit: 1000,
        },
        memorialsError: null,
        memorialsLoading: false,
      };
    },

    created() {
      const vm = this;

      // fetch initial set of memorials
      this.fetchMemorials();

      // bind back/forward button to event handler
      window.onpopstate = this.onPopState;
    },

    watch: {

      mapState (newMapState) {
        console.log(newMapState);
      },

      /**
       * Navigates to the memorial detail view if a memorial becomes selected.
       * Defaults to the filter/map view.
       * @param newMemorial The newly selected memorial or none.
       * @param oldMemorial
       */
      memorial (newMemorial, oldMemorial) {
        const vm = this;
        let route = {name: 'map', params: this.$route.params};

        if (newMemorial) {
          route = {
            name: 'memorial-detail',
            params: {
              ...this.$route.params,
                id: newMemorial.id
            }
          };
        }

        vm.$router.push(route);
      }
    },

    methods: {

      onMapMoveEnd(center, zoom) {
        const vm = this;
        const mapState = mapCenterToPath(center, zoom);

        if (vm.historyAction) {
          vm.historyAction = false;
          return;
        }

        this.$router.push({name: this.$route.name, params: { mapState }});
      },

      fetchMemorials() {
        const vm = this;
        vm.api
          .getMemorials(vm.memorialFilters)
          .then(json => vm.memorials = json.results);
      },

      setFilterParam(param, value) {
        const vm = this;
        vm.memorialFilters[param] = value;
        vm.fetchMemorials();
      },

      selectMemorial(memorialId) {
        const vm = this;

        if (!memorialId) {
          vm.memorial = null;
          return;
        }

        vm.memorialLoading = true;
        vm.api
          .getMemorial(memorialId)
          .then(json => {
            vm.memorial = json;
            vm.memorialLoading = false;
          });
      },

      onAuthorChange(author) {
        const vm = this;
        vm.setFilterParam('author', author);
      },

      onFilterChange(param, value) {
        const vm = this;
        vm.setFilterParam(param, value);
      },

      onPopState() {
        const vm = this;
        const newInitialView = pathToMapCenter(vm.mapState);
        if (newInitialView) {
          vm.historyAction = true;
          vm.initialView = newInitialView;
        }
      }
    }
  };

</script>
