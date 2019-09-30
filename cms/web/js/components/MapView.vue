<template>
  <div class="MapView row">

    <main class="col p-0">
      <Map
        :initial-map-state="initialMapState"
        :features="memorials"
        v-on:select="onMapSelect"
        v-on:moveend="onMapMoveEnd"></Map>
    </main>

    <aside
      v-if="$route.name === 'map'"
      class="Sidebar col-6 col-lg-4 border-bottom border-sm-bottom-0 border-sm-left order-first order-sm-last pt-2">
      <h5>{{ 'Keyword search' | translate }}</h5>
      <filter-list
        v-on:change="onAuthorSelectionChange"
        :items="authorFilterList"
        :selection="authorSelection"
        :initial-collapse="false"
      >
        <template v-slot:header>{{ authorFilterHeader }}</template>
      </filter-list>

      <filter-list
        v-on:change="onTypeSelectionChange"
        :items="typeFilterList"
        :selection="typeSelection">
        <template v-slot:header>{{ typeFilterHeader }}</template>
      </filter-list>
    </aside>

    <aside
      v-if="$route.name === 'memorial-detail'"
      class="Sidebar col-6 col-lg-4 border-bottom border-sm-bottom-0 border-sm-left order-first order-sm-last p-0"
    >
      <memorial-card
        v-if="memorialSelect"
        class="border-0"
        :banner="memorialSelect.banner"
        :title="memorialSelect.name"
        :position="memorialSelect.position"
        :authors="memorialSelect.authors"
        :address="memorialSelect.address"
        :contactInfo="memorialSelect.contact_info"
        :directions="memorialSelect.directions"
        :introduction="memorialSelect.introduction"
        v-on:hide="onMemorialDetailHide">
      </memorial-card>
    </aside>

  </div>
</template>

<script>
  import {mapStateToPath, pathToMapState} from '../utils';
  import Map from './Map.vue';
  import FilterList from './FilterList.vue';
  import MemorialCard from './MemorialCard.vue';
  import api from '../Api';
  import translate from '../translate';

  export default {
    props: {
      mapStatePath: {
        type: String,
        default: '@14.9304,50.625,7z'
      },
      memorialId: [String, Number],
    },

    components: {
      MemorialCard,
      Map,
      FilterList,
    },

    filters: {
      translate,
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

      memorialParams () {
        return {
          author: [...this.authorSelection],
          memorial_type: [...this.typeSelection],
          ordering: 'name',
          limit: 1000,
        };
      },

      authorFilterHeader () {
        const vm = this;
        return `${translate('Authors')} (${vm.authorSelection.size} / ${vm.authors.length})`;
      },

      authorFilterList () {
        return this.authors.map(x => ({
          id: x.id,
          title: `${x.last_name}, ${x.first_name}`,
        }));
      },

      authorParams () {
        return {
          ordering: 'last_name,first_name',
          limit: 1000,
        };
      },

      typeFilterHeader () {
        const vm = this;
        return `${translate('Types')} (${vm.typeSelection.size} / ${vm.types.length})`;
      },

      typeFilterList () {
        return this.types.map(x => ({
          id: x.id,
          title: x.name,
        }));
      },

      typeParams () {
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

      memorialParams (newFilters) {
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

        vm.$router.push({
          name: vm.$route.name,
          params: { ...vm.$route.params, mapStatePath }},
          () => {}
        );
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
          .getMemorials(vm.memorialParams)
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
          .getAuthors(vm.authorParams)
          .then(json => vm.authors = json.results);
      },

      fetchTypes() {
        const vm = this;
        api
          .getResults('/memorialTypes', vm.typeParams)
          .then(json => vm.types = json.results);
      }
    }
  };
</script>

<style lang="scss">
  .MapView {
    height: 80vh;
    max-height: 80vh;

    .Map {
      max-height: 80vh;
    }

    .Sidebar {
      max-height: 80vh;
      overflow-x: scroll;
    }
  }
</style>
