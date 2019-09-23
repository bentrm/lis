<template>
  <div class="Map"></div>
</template>

<script>
  import L from 'leaflet';
  import 'leaflet.locatecontrol';
  import 'leaflet.markercluster';
  import Extent from '../leaflet.extentcontrol';
  import marker from '../markers';

  export default {

    props: {
      initialView: Object,
      memorial: Object,
      memorials: Array,
    },

    data () {
      return {
        selectedMarker: null,
      }
    },

    mounted () {
      const vm = this;
      const attribution =
          'Rendering <a href="https://geoinformatik.htw-dresden.de">'
        + 'Labor Geoinformatik (HTWD, Fak. GI)</a> | Map data &copy; '
        + '<a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, '
        + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
      const osmLayer = L.tileLayer.wms(
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

      vm.clusterLayer.on('click', ({layer}) => {
        this.$emit('click', layer.options.id);
      });

      vm.map = L.map(vm.$el, {
        center: vm.initialCenter,
        layers: [osmLayer, vm.clusterLayer],
        zoom: vm.initialZoom,
      });

      vm.map.on('click', () => {
        this.$emit('click', null);
      });

      vm.map.on('moveend', () => {
        const {lat, lng} = vm.map.getCenter();
        vm.$emit('moveend', [lng, lat], vm.map.getZoom());
      });

      const scaleControl = L.control.scale();
      scaleControl.addTo(vm.map);

      const extentControl = new Extent({
        layer: vm.clusterLayer
      });
      extentControl.addTo(vm.map);

      const locateControl = L.control.locate({
        flyTo: true,
        icon: 'fas fa-location-arrow',
        iconLoading: 'fas fa-spinner fa-spin',
        iconElementTag: 'i',
        locateOptions: {
          enableHighAccuracy: true,
        },
        showPopup: false,
      });
      locateControl.addTo(vm.map);

    },

    watch: {

      initialView ({center, zoom}, oldView) {
        const vm = this;
        vm.map.flyTo(center, zoom);
      },

      selectedMarker (newSelectedMarker, oldSelectedMarker) {
        if (oldSelectedMarker) {
          const oldElement = oldSelectedMarker.getElement();
          oldSelectedMarker.getElement().classList.remove('leaflet-marker-icon-selected');
        }
        if (newSelectedMarker) {
          newSelectedMarker.getElement().classList.add('leaflet-marker-icon-selected');
        }
      },

      memorial (newMemorial, oldMemorial) {
        const vm = this;

        if (newMemorial) {
          vm.map.eachLayer(layer => {
            if (layer.options.id === newMemorial.id) {
              vm.selectedMarker = layer;
            }
          })
        } else {
          vm.selectedMarker = null;
        }
      },

      memorials (newMemorials, oldMemorials) {
        const vm = this;
        const newMarkers = newMemorials.map(({position: [lng, lat], memorial_types, ...otherProps}) => {
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
        vm.map.fitBounds(vm.clusterLayer.getBounds());
      }
    }
  };
</script>
