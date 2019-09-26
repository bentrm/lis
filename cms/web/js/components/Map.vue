<template>
  <div class="Map"></div>
</template>

<script>
  import L from 'leaflet';
  import 'leaflet.locatecontrol';
  import 'leaflet.markercluster';
  import Extent from '../leaflet.extentcontrol';
  import marker from '../markers';

  const attribution =
    'Rendering <a href="https://geoinformatik.htw-dresden.de">'
    + 'Labor Geoinformatik (HTWD, Fak. GI)</a> | Map data &copy; '
    + '<a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, '
    + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';

  export default {

    props: {
      initialMapState: Object,
      features: Array,
    },

    created () {
      const vm = this;
      vm.osmLayer = L.tileLayer.wms(
        'https://kosm.geoinformation.htw-dresden.de/geoserver/osm/wms',
        {
          attribution,
          format: 'image/png',
          format_options: 'dpi:180',
          layers: 'osm:OSM',
          tiled: true,
          tileSize: 256,
          transparent: true,
          version: '1.3.0',
          detectRetina: true,
        },
      );
      vm.clusterLayer = L.markerClusterGroup({
        animate: true,
        polygonOptions: {
          color: '#69140e'
        },
        spiderLegPolylineOptions: {
          color: '#69140e'
        }
      });
      vm.scaleControl = L.control.scale();
      vm.extentControl = new Extent({
        layer: vm.clusterLayer
      });
      vm.locateControl = L.control.locate({
        flyTo: true,
        icon: 'fas fa-location-arrow',
        iconLoading: 'fas fa-spinner fa-spin',
        iconElementTag: 'i',
        locateOptions: {
          enableHighAccuracy: true,
        },
        showPopup: false,
      });
    },

    mounted () {
      const vm = this;
      const {center, zoom} = vm.initialMapState;
      const map = vm.map = L.map(vm.$el, {
        center, zoom,
        layers: [
          vm.osmLayer,
          vm.clusterLayer
        ],
      });
      vm.scaleControl.addTo(map);
      vm.locateControl.addTo(map);
      vm.extentControl.addTo(map);

      map.on('click', vm.onMapClick);
      map.on('moveend', vm.onMoveEnd);
      vm.clusterLayer.on('click', vm.onFeatureSelect);
    },

    watch: {

      /**
       * Describes the inital map center and zoom.
       * @param center
       * @param zoom
       */
      initialMapState ({center, zoom}) {
        this.map.flyTo(center, zoom);
      },

      features (newFeatures) {
        const vm = this;
        const newMarkers = newFeatures.map(feature => {
          const {position: [lng, lat], memorial_types, ...otherProps} = feature;
          const memorialType = memorial_types[0].id;
          return L.marker([lat, lng], {
            icon: L.divIcon({
              className: 'fa-leaflet-icon',
              html: marker(memorialType).html,
            }),
            ...otherProps
          });
        });

        vm.clusterLayer.clearLayers();
        vm.clusterLayer.addLayers(newMarkers);
      }
    },

    methods: {

      onMapClick () {
        this.$emit('select', null);
      },

      onMoveEnd () {
        const vm = this;
        const {lat, lng} = vm.map.getCenter();
        vm.$emit('moveend', [lng, lat], vm.map.getZoom());
      },

      onFeatureSelect ({layer}) {
        this.$emit('select', layer.options.id);
      }

    }
  };
</script>

<style lang="scss">
  @import "~leaflet/dist/leaflet";
  @import "~leaflet.locatecontrol/src/L.Control.Locate";
  @import "../../scss/marker";
</style>
