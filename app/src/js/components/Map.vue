<template>
  <div class="Map">
    <l-map
      ref="mapRef"
      :zoom="zoom"
      :center="center"
      :maxBounds="maxBounds"
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
          :icon="getMarkerIcon(feature)"
          :options="feature"
          @click="onMarkerClick"
        >
          <l-popup>{{feature.name}}</l-popup>
        </l-marker>
      </l-marker-cluster>
    </l-map>
  </div>
</template>

<script>
import { LMap, LMarker, LControlScale, LPopup } from 'vue2-leaflet';
import LMarkerCluster from 'vue2-leaflet-markercluster';
import LLayerExtent from './LayerExtent.vue';
import LLocateControl from './LocateControl.vue';
import TiledWmsLayer from './TiledWmsLayer.vue';
import { DivIcon } from 'leaflet';
import marker from '../markers';

export default {
  props: {
    initialMapState: Object,
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
    const retina =
      (window.devicePixelRatio ||
        window.screen.deviceXDPI / window.screen.logicalXDPI) > 1;
    return {
      baseUrl: 'https://kosm.geoinformation.htw-dresden.de/geoserver/osm/wms',
      layers: 'osm:OSM',
      maxBounds: [[35.0, -10.0], [65.0, 30.0]],
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
        animate: true,
        polygonOptions: {
          color: '#69140e'
        },
        spiderLegPolylineOptions: {
          color: '#69140e'
        }
      }
    };
  },

  computed: {
    center() {
      const vm = this;
      const { center } = vm.initialMapState;
      return center;
    },

    zoom() {
      const vm = this;
      const { zoom } = vm.initialMapState;
      return zoom;
    },

    layerExtentOptions() {
      if (this.$refs.clusterRef) {
        return {
          layer: this.$refs.clusterRef.mapObject
        };
      }
    }
  },

  watch: {
    /**
     * Describes the inital map center and zoom.
     * Updates the map position if the given initial zoom state differs from the
     * actual map state.
     * @param center
     * @param zoom
     */
    // initialMapState({ center, zoom }) {
    //   const newCenter = !this.map.getCenter().equals(L.latLng(center), 0.001);
    //   const newZoom = this.map.getZoom() != zoom;
    //   if (newCenter || newZoom) {
    //     this.map.flyTo(center, zoom);
    //   }
    // },
    // features(newFeatures) {
    //   this.addFeatures();
    // }
  },

  methods: {
    getMarkerIcon(feature) {
      const { memorial_types: memorialTypes } = feature;
      return new DivIcon({
        className: 'fa-leaflet-icon',
        html: marker(memorialTypes[0].id).html
      });
    },

    onMapMoveEnd() {
      const vm = this;
      const { lat, lng } = vm.$refs.mapRef.mapObject.getCenter();
      vm.$emit('moveend', [lng, lat], vm.$refs.mapRef.mapObject.getZoom());
    },

    onMarkerClick({ target }) {
      console.log(target);
      this.$emit('select', target.options.id);
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/marker';

.Map {
  padding: 0;
  height: 100%;
  width: 100%;
}
</style>
