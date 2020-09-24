<template>
  <div class="container-fluid">
    <div class="MapView row">
      <main v-if="!isSmallDevice" class="col p-0">
        <map-component
          :map-position="mapPosition"
          :max-bounds="mapMaxBounds"
          :features="memorials"
          :initialExtent="initialExtent"
          :featureExtent="featureExtent"
          @click="onMapSelect"
        />
      </main>

      <b-card class="Sidebar col col-md-5 col-lg-4 p-0" no-body>
        <b-card-header header-tag="nav">
          <b-nav pills justified class="small">
            <b-nav-item :to="{ name: 'map' }" v-if="isSmallDevice" :active="isSmallDevice && $route.name === 'map'">
              <i class="fas fa-map"></i>
              {{ 'Map' | translate }} ({{ memorials.length }})
            </b-nav-item>
            <b-nav-item :to="{ name: 'map-filter' }" :active="!isSmallDevice && $route.name === 'map' || $route.name === 'map-filter'">
              <i class="fas fa-search"></i>
              {{ 'Filters' | translate }}
            </b-nav-item>
            <b-nav-item :to="{ name: 'map-detail', params: { memorialId: memorial.id } }" v-if="memorial" :active="$route.name === 'map-detail'">
              <i class="fas" :class="memorialTabIconClassName"></i>
              {{ memorialTabTitle }}
            </b-nav-item>
          </b-nav>
        </b-card-header>
        <b-card-body class="m-0 p-0">
          <div v-if="isSmallDevice">
            <keep-alive>
              <map-component
                v-if="$route.name === 'map'"
                :map-position="mapPosition"
                :max-bounds="mapMaxBounds"
                :features="memorials"
                :initialExtent="initialExtent"
                :featureExtent="featureExtent"
                @click="onMapSelect"
              />
            </keep-alive>
          </div>

          <div v-if="!isSmallDevice && $route.name === 'map' || $route.name === 'map-filter'" class="p-3">
            <filter-list
              @change="onAuthorSelectionChange"
              :items="authors"
              :to-searchable-string="author => author.also_known_as[0].first_name + ' ' + author.also_known_as[0].last_name"
              :selection="authorSelection"
              :initial-collapse="false"
            >
              <template v-slot:header>{{ authorFilterHeader }}</template>
              <template v-slot:item="slotProps">
                {{ [slotProps.item.title, slotProps.item.first_name, slotProps.item.last_name].filter(x => x).join(' ') }}
              </template>
            </filter-list>

            <filter-list
              @change="onTypeSelectionChange"
              :items="typeFilterList"
              :selection="typeSelection"
            >
              <template v-slot:header>{{ typeFilterHeader }}</template>
            </filter-list>
          </div>

          <memorial-card
            v-else-if="memorial && $route.name === 'map-detail'"
            class="border-0"
            :id="memorial.id"
            :banner="memorial.banner"
            :title="memorial.name"
            :image="memorial.title_image"
            :position="memorial.position"
            :authors="memorial.authors"
            :address="memorial.address"
            :contact-info="memorial.contact_info"
            :directions="memorial.directions"
            :introduction="memorial.introduction"
            :description="memorial.description"
            :detailed-description="memorial.detailed_description"
          />
        </b-card-body>
      </b-card>
    </div>
  </div>
</template>

<script>
import api from '../Api';
import translate from '../translate';
import {getDeviceWidth} from '../utils';
import FilterList from '../components/FilterList.vue';
import MapComponent from '../components/Map.vue';
import MemorialCard from '../components/MemorialCard.vue';
import {iconClassName} from '../markers';
import AuthorName from '../components/AuthorName.vue';
import SearchBar from '../components/SearchBar.vue';

const fetchMemorials = async (params = { limit: 1000 }) => api
      .getMemorials(params)
      .then(({bbox, results}) => ({
        memorials: results,
        extent: [[bbox[0][1], bbox[0][0]], [bbox[1][1], bbox[1][0]]],
      }));

  const fetchAuthors = async (params = { ordering: 'last_name,first_name', limit: 1000}) => api
    .getAuthors(params)
    .then(({results}) => results);

  const fetchTypes = async (params = { ordering: 'name', limit: 1000 }) => api
      .getResults('/memorialTypes', params)
      .then(({results}) => results);

  export default {
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
        memorial: undefined,

        // authors
        authors: [],
        authorSelection: new Set(),

        // types
        types: [],
        typeSelection: new Set(),

        initialExtent: null,
        featureExtent: [{lng: -10.0, lat: 35.0 }, { lng: 30.0, lat: 65.0 }],
        mapPosition: {
          center: { lng: 13.6811, lat: 51.0526 },
          zoom: 8,
        },
        mapMaxBounds: [{lng: -10.0, lat: 35.0 }, { lng: 30.0, lat: 65.0 }],
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

      memorialTabTitle() {
        const name = this.memorial ? this.memorial.name : '';

        if (name.length > 20) {
          return name.substr(0, 20).trim() + '…';
        }

        return name;
      },

      memorialTabIconClassName() {
        if (this.memorial) {
          const symbolId = this.memorial.memorial_types[0].id;
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
      }
    },

    watch: {
      async memorialParams(newFilters) {
        const vm = this;
        const {memorials, extent} = await fetchMemorials(newFilters);
        vm.memorials = memorials;
        vm.featureExtent = extent;
      }
    },

    async beforeRouteEnter (to, from, next) {
      const memorialId = to.name === 'map-detail' ? to.params.memorialId : null;
      const [{extent, memorials}, memorial, authors, types] = await Promise.all([
        fetchMemorials(),
        memorialId ? api.getMemorial(memorialId) : null,
        fetchAuthors(),
        fetchTypes(),
      ]);

      next(vm => {
        vm.memorials = memorials;
        vm.featureExtent = extent;
        vm.authors = authors;
        vm.types = types;

        if (memorial) {
          vm.memorial = memorial;
          vm.mapPosition = {
            center: {lat: memorial.position[1], lng: memorial.position[0] },
            zoom: 18,
          }
        } else {
          vm.initialExtent = extent;
        }
      });
    },

    async beforeRouteUpdate (to, from, next) {
      const vm = this;
      const memorialId = to.name === 'map-detail' ? to.params.memorialId : null;

      if (memorialId) {
        await vm.fetchMemorial(memorialId);
        vm.mapPosition = {
          center: { lat: vm.memorial.position[1], lng: vm.memorial.position[0] },
          zoom: 18,
        }
      }
      next();
    },

    mounted() {
      const vm = this;
      window.onresize = vm.onWindowResize;
    },

    methods: {
      async fetchMemorial(memorialId) {
        const vm = this;
        vm.memorial = await api.getMemorial(memorialId);
      },

      async onMapSelect(feature) {
        const vm = this;
        const {options: { id }} = feature;

        if (vm.isSmallDevice) {
          await vm.fetchMemorial(id);
          vm.mapPosition = { center: feature.getLatLng(), zoom: 18 };
        } else {
          vm.$router.push({
              name: 'map-detail',
              params: { ...vm.$route.params, memorialId: id }
            })
            .catch(() => {});
        }
      },

      onWindowResize() {
        this.isSmallDevice = getDeviceWidth() < 768;
      },

      onAuthorSelectionChange(selection) {
        this.authorSelection = selection;
      },

      onTypeSelectionChange(selection) {
        this.typeSelection = selection;
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
