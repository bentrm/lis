<template>
  <div class="container-fluid">
    <div class="MapView row">
      <main v-if="!isSmallDevice" class="col p-0">
        <map-component
          :center="$store.state.mapCenter"
          :zoom="$store.state.mapZoom"
          :max-bounds="$store.state.mapMaxBounds"
          :features="memorials"
          @select="onMapSelect"
          @moveend="onMapMoveEnd"
        ></map-component>
      </main>

      <b-card class="Sidebar col col-md-5 col-lg-4 p-0" no-body>
        <b-tabs card pills small fill lazy :value="activeTabIndex" @activate-tab="onActivateTab">
          <b-tab :active="$route.name === 'map'" no-body v-if="isSmallDevice">
            <template v-slot:title>
              <i class="fas fa-map"></i>
              {{ 'Map' | translate }} ({{ memorials.length }})
            </template>
            <map-component
              :center="$store.state.mapCenter"
              :zoom="$store.state.mapZoom"
              :max-bounds="$store.state.mapMaxBounds"
              :features="memorials"
              @select="onMapSelect"
              @moveend="onMapMoveEnd"
            ></map-component>
          </b-tab>

          <b-tab>
            <template v-slot:title>
              <i class="fas fa-search"></i>
              {{ 'Filters' | translate }}
            </template>
            <filter-list
              @change="onAuthorSelectionChange"
              :items="authors"
              :to-searchable-string="author => author.also_known_as[0].first_name + ' ' + author.also_known_as[0].last_name"
              :selection="authorSelection"
              :initial-collapse="false"
            >
              <template v-slot:header>{{ authorFilterHeader }}</template>
              <template v-slot:item="slotProps">
                <author-name :show-details="false" :isPseudonym="slotProps.item.also_known_as[0].is_pseudonym" :title="slotProps.item.also_known_as[0].title" :firstName="slotProps.item.also_known_as[0].first_name" :lastName="slotProps.item.also_known_as[0].last_name" />
              </template>
            </filter-list>

            <filter-list
              @change="onTypeSelectionChange"
              :items="typeFilterList"
              :selection="typeSelection"
            >
              <template v-slot:header>{{ typeFilterHeader }}</template>
            </filter-list>
          </b-tab>

          <b-tab :active="$route.name === 'memorial-detail'" v-if="memorialSelect" no-body>
            <template v-slot:title>
              <i class="fas fa-monument"></i>
              {{ 'Memorial' | translate }}
            </template>
            <memorial-card
              class="border-0"
              :id="memorialId"
              :banner="memorialSelect.banner"
              :title="memorialSelect.name"
              :image="memorialSelect.title_image"
              :position="memorialSelect.position"
              :authors="memorialSelect.authors"
              :address="memorialSelect.address"
              :contact-info="memorialSelect.contact_info"
              :directions="memorialSelect.directions"
              :introduction="memorialSelect.introduction"
              :description="memorialSelect.description"
              :detailed-description="memorialSelect.detailed_description"
            ></memorial-card>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
  import api from '../Api';
  import translate from '../translate';
  import {getDeviceWidth, mapStateToPath} from '../utils';
  import FilterList from '../components/FilterList.vue';
  import MapComponent from '../components/Map.vue';
  import MemorialCard from '../components/MemorialCard.vue';
  import {iconClassName} from '../markers';
  import AuthorName from '../components/AuthorName.vue';
  import SearchBar from '../components/SearchBar.vue';

  const tabs = {
  '#filter': 1,
  '#detail': 2
};

const tabIndex = hash => {
  return tabs[hash] || 0;
};

const tabHash = index => {
  return Object.keys(tabs).find(key => tabs[key] === index) || '';
};

export default {
  props: {
    memorialId: [String, Number]
  },

  components: {
    AuthorName,
    MemorialCard,
    MapComponent,
    FilterList,
    SearchBar,
  },

  filters: {
    translate
  },

  metaInfo: {
    title: translate('Map'),
  },

  data() {
    return {
      isSmallDevice: getDeviceWidth() < 768,

      memorials: [],
      memorialSelect: undefined,

      // authors
      authors: [],
      authorSelection: new Set(),

      // types
      types: [],
      typeSelection: new Set()
    };
  },

  computed: {
    memorialParams() {
      return {
        author: [...this.authorSelection],
        memorial_type: [...this.typeSelection],
        limit: 1000
      };
    },

    activeTabIndex() {
      return tabIndex(this.$route.hash);
    },

    memorialTabTitle() {
      const name = this.memorialSelect ? this.memorialSelect.name : '';

      if (name.length > 20) {
        return name.substr(0, 20).trim() + '…';
      }

      return name;
    },

    memorialTabIconClassName() {
      if (this.memorialSelect) {
        const symbolId = this.memorialSelect.memorial_types[0].id;
        return iconClassName(symbolId);
      }
      return '';
    },

    authorFilterHeader() {
      const vm = this;
      return `${translate('Authors')} (${vm.authorSelection.size} / ${
        vm.authors.length
      })`;
    },

    authorFilterList() {
      return this.authors.map(x => ({
        id: x.id,
        title: `${x.last_name}, ${x.first_name}`
      }));
    },

    authorParams() {
      return {
        ordering: 'last_name,first_name',
        limit: 1000
      };
    },

    typeFilterHeader() {
      const vm = this;
      return `${translate('Types')} (${vm.typeSelection.size} / ${
        vm.types.length
      })`;
    },

    typeFilterList() {
      return this.types.map(x => ({
        id: x.id,
        title: x.name
      }));
    },

    typeParams() {
      return {
        ordering: 'name',
        limit: 1000
      };
    }
  },

  watch: {
    memorialId(newMemorialId) {
      const vm = this;
      if (newMemorialId) {
        vm.fetchMemorial();
      } else {
        vm.memorialSelect = null;
      }
    },

    memorialParams(newFilters) {
      this.fetchMemorials();
    }
  },

  mounted() {
    const vm = this;

    vm.fetchMemorials();
    vm.fetchAuthors();
    vm.fetchTypes();

    if (vm.memorialId) {
      vm.fetchMemorial();
    }

    window.onresize = vm.onWindowResize;
    window.onpopstate = vm.onWindowPopState;
  },

  methods: {
    onActivateTab(index) {
      const vm = this;
      const hash = tabHash(index);

      vm.$router
        .replace({
          ...vm.$router.params,
          hash
        })
        .catch(() => {});
    },

    onMapSelect(memorialId) {
      const vm = this;

      if (memorialId) {
        vm.$router
          .push({
            name: 'memorial-detail',
            params: { ...vm.$route.params, memorialId },
            hash: '#detail'
          })
          .catch(() => {});
      } else {
        vm.$router
          .push({
            name: 'map',
            params: { ...vm.$route.params },
            hash: ''
          })
          .catch(() => {});
      }
    },

    onWindowResize() {
      this.isSmallDevice = getDeviceWidth() < 768;
    },

    onWindowPopState() {
      this.$store.commit('syncMapState', {route: this.$route});
    },

    onMapMoveEnd(center, zoom) {
      const vm = this;
      const mapStatePath = mapStateToPath(center, zoom);

      if (!vm.$store.state.syncingMapState) {
        vm.$router.push(
          {
            ...vm.$route,
            name: vm.$route.name,
            params: { ...vm.$route.params, mapStatePath }
          },
          () => {}
        );
        vm.$store.commit('logMapState', {route: vm.$route});
      } else {
        vm.$store.commit('endSyncMapState', {route: vm.$route});
      }
    },

    onAuthorSelectionChange(selection) {
      this.authorSelection = selection;
    },

    onTypeSelectionChange(selection) {
      this.typeSelection = selection;
    },

    fetchMemorials() {
      const vm = this;
      api
        .getMemorials(vm.memorialParams)
        .then(json => (vm.memorials = json.results));
    },

    fetchMemorial() {
      const vm = this;
      api.getMemorial(vm.memorialId).then(json => (vm.memorialSelect = json));
    },

    fetchAuthors() {
      const vm = this;
      api.getAuthors(vm.authorParams).then(json => (vm.authors = json.results));
    },

    fetchTypes() {
      const vm = this;
      api
        .getResults('/memorialTypes', vm.typeParams)
        .then(json => (vm.types = json.results));
    }
  }
};
</script>

<style lang="scss">
@media (max-width: 768px) {
  .Map {
    height: 200px;
    height: 100vw;
  }
}

@media (min-width: 576px) {
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
}
</style>
