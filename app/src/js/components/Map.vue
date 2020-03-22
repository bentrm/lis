<template>
  <div class="Map">
    <l-map ref="mapRef" :max-bounds="maxBounds">
      <l-control-scale position="bottomleft" :imperial="true" :metric="true"/>
      <l-layer-extent :extent="featureExtent"/>
      <l-locate-control :options="locateControlOptions"/>
      <tiled-wms-layer
        :base-url="baseUrl"
        :layers="layers"
        format="image/png"
        version="1.3.0"
        :attribution="attribution"
        :detect-retina="true"
        :tiled="true"
        :format_options="format_options"
        :transparent="true"
      />
      <l-marker-cluster :options="markerClusterOptions" ref="clusterRef">
        <l-marker
          v-for="feature in features"
          :key="feature.id"
          :lat-lng="[feature.position[1], feature.position[0]]"
          :icon="getMarkerIcon(feature)"
          :options="{id: feature.id, title: feature.name, alt: feature.name}"
          @click="onMarkerClick"
          @dblclick="onMarkerDblClick"
          @keydown="onMarkerClick"
        >
          <l-tooltip :options="{direction: 'top', offset: [0, -10]}">{{ feature.name }}</l-tooltip>
        </l-marker>
      </l-marker-cluster>
    </l-map>
  </div>
</template>

<script>
  import {LControlScale, LMap, LMarker, LPopup, LTooltip} from 'vue2-leaflet';
  import LMarkerCluster from 'vue2-leaflet-markercluster/dist/Vue2LeafletMarkercluster';
  import LLayerExtent from './LayerExtent.vue';
  import LLocateControl from './LocateControl.vue';
  import TiledWmsLayer from './TiledWmsLayer.vue';
  import {DivIcon} from 'leaflet';
  import marker from '../markers';

  const iconCache = {};

export default {
  props: {
    isSmallDevice: Boolean,
    mapPosition: Object,
    maxBounds: Array,
    features: Array,
    initialExtent: Array,
    featureExtent: Array,
  },

  components: {
    LMap,
    TiledWmsLayer,
    LMarker,
    LTooltip,
    LMarkerCluster,
    LLayerExtent,
    LControlScale,
    LLocateControl,
    LPopup
  },

  data() {
    const retina =
      (window.devicePixelRatio ||
        window.screen.deviceXDPI / window.screen.logicalXDPI) > 1;
    return {
      baseUrl: 'https://kosm.geoinformation.htw-dresden.de/geoserver/osm/wms',
      layers: 'osm:OSM',
      format_options: retina ? 'dpi:180' : 'dpi:90',
      attribution:
        'Rendering <a href="https://geoinformatik.htw-dresden.de">' +
        'Labor Geoinformatik (HTWD, Fak. GI)</a> | Map data &copy; ' +
        '<a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
      locateControlOptions: {
        flyTo: true,
        icon: 'fas fa-location-arrow',
        iconLoading: 'fas fa-spinner fa-spin',
        iconElementTag: 'i',
        locateOptions: {
          enableHighAccuracy: true
        },
        showPopup: false
      },
      markerClusterOptions: {
        animate: false,
        maxClusterRadius: 40,
        polygonOptions: {
          color: '#69140e'
        },
        spiderLegPolylineOptions: {
          color: '#69140e'
        }
      }
    };
  },

  mounted() {
    const vm = this;
    vm.$nextTick(() => {
      if (vm.mapPosition) {
        vm.setMapView();
      } else {
        vm.setMapViewFromExtent();
      }
    })
  },

  watch: {
    mapPosition() {
      this.setMapView();
    },

    initialExtent(newExtent) {
      this.setMapViewFromExtent();
    }
  },

  computed: {
    layerExtentOptions() {
      if (this.$refs.clusterRef) {
        return {
          layer: this.$refs.clusterRef.mapObject
        };
      }
    }
  },

  methods: {
    setMapView() {
      const vm = this;
      const map = vm.$refs.mapRef.mapObject;
      const {center, zoom} = vm.mapPosition;
      map.flyTo(center, zoom, { duration: .8, easeLinearity: 1 });
    },

    setMapViewFromExtent() {
      const map = this.$refs.mapRef.mapObject;
      map.fitBounds(this.initialExtent);
    },

    getMarkerIcon(feature) {
      const id = feature.memorial_types[0].id;

      if (!iconCache[id]) {
        iconCache[id] = marker(id);
      }

      return new DivIcon({
        className: 'fa-leaflet-icon',
        html: iconCache[id].html
      });
    },

    onMarkerClick({ target }) {
      this.$emit('click', target);
    },

    onMarkerDblClick({ target }) {
      this.$emit('dblclick', target);
    },
  }
};
</script>

<style lang="scss">
@import '~leaflet/dist/leaflet.css';
@import '../../scss/marker';

.Map {
  padding: 0;
  height: 100%;
  width: 100%;
}

.leaflet-marker-icon {
  .drop-shadow {
    filter: drop-shadow(0 0 2px rgba(0, 0, 0, .7));
    transition: filter 0.2s ease-in-out;

    &:hover {
      filter: drop-shadow(0 0 5px rgba(0, 0, 0, .7));
    }
  }

  &.leaflet-marker-icon-selected .drop-shadow {
    filter: drop-shadow(0 0 10px rgba(163, 22, 33, .7));
  }

}

.leaflet-control-attribution a {
  color: theme-color('primary');
}
</style>
