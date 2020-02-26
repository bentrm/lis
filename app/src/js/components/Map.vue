<template>
  <div class="Map">
    <l-map
      ref="mapRef"
      :center="center"
      :zoom="zoom"
      :max-bounds="maxBounds"
      @moveend="onMapMoveEnd"
    >
      <l-control-scale position="bottomleft" :imperial="true" :metric="true"></l-control-scale>
      <l-layer-extent :layer="$refs.clusterRef ? $refs.clusterRef.mapObject : null"></l-layer-extent>
      <l-locate-control :options="locateControlOptions"></l-locate-control>
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
      ></tiled-wms-layer>
      <l-marker-cluster :options="markerClusterOptions" ref="clusterRef">
        <l-marker
          v-for="feature in features"
          :key="feature.id"
          :lat-lng="[feature.position[1], feature.position[0]]"
          :icon="getMarkerIcon(feature.memorial_types[0].id)"
          :options="feature"
          @click="onMarkerClick"
          @keydown="onMarkerClick"
        ></l-marker>
      </l-marker-cluster>
    </l-map>
  </div>
</template>

<script>
  import {LControlScale, LMap, LMarker, LPopup} from 'vue2-leaflet';
  import LMarkerCluster from 'vue2-leaflet-markercluster/dist/Vue2LeafletMarkercluster';
  import LLayerExtent from './LayerExtent.vue';
  import LLocateControl from './LocateControl.vue';
  import TiledWmsLayer from './TiledWmsLayer.vue';
  import {DivIcon} from 'leaflet';
  import marker from '../markers';

  const iconCache = {};

export default {
  props: {
    center: Object,
    zoom: Number,
    maxBounds: Array,
    features: Array
  },

  components: {
    LMap,
    TiledWmsLayer,
    LMarker,
    LMarkerCluster,
    LLayerExtent,
    LControlScale,
    LLocateControl,
    LPopup
  },

  data() {
    const vm = this;
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

  watch: {
    center(newCenter) {
      this.setMapView();
    },

    zoom(newZoom) {
      this.setMapView();
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
      const map = this.$refs.mapRef.mapObject;
      map.flyTo(this.center, this.zoom);
    },

    getMarkerIcon(id) {
      if (!iconCache[id]) {
        iconCache[id] = marker(id);
      }
      return new DivIcon({
        className: 'fa-leaflet-icon',
        html: iconCache[id].html
      });
    },

    onMapMoveEnd() {
      const vm = this;
      const center = vm.$refs.mapRef.mapObject.getCenter();
      vm.$emit('moveend', center, vm.$refs.mapRef.mapObject.getZoom());
    },

    onMarkerClick({ target }) {
      this.$emit('select', target.options.id);
    }
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
