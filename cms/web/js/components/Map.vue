<template>
  <div class="Map"></div>
</template>

<script>
  import {icon, layer} from '@fortawesome/fontawesome-svg-core';
  import {
    faArchive,
    faBirthdayCake,
    faBook,
    faBuilding,
    faChurch,
    faCross,
    faGraduationCap,
    faInfo,
    faLandmark,
    faLightbulb,
    faMapMarker,
    faMonument,
    faMountain,
    faPalette,
    faRoad,
    faSquare
  } from '@fortawesome/free-solid-svg-icons';
  import L from 'leaflet';
  import 'leaflet.locatecontrol';
  import 'leaflet.markercluster';


  const symbols = {
    16: faBuilding,
    17: faRoad,
    18: faBirthdayCake,
    19: faBuilding,
    20: faCross,
    21: faLightbulb,
    22: faMonument,
    23: faMonument,
    24: faSquare,
    25: faLandmark,
    26: faGraduationCap,
    27: faChurch,
    28: faMountain,
    29: faMonument,
    30: faPalette,
    31: faInfo,
    32: faPalette,
    33: faBook,
    34: faArchive
  };

  const symbolLayer = symbolId => {
    const symbol = symbols[symbolId] || faMonument;

    return layer(push => {
      push(icon(faMapMarker, {
        styles: {'color': '#69140e'},
        transform: {size: 48, x: 0, y: 0},
      }));
      push(icon(symbol, {
        styles: {'color': 'white'},
        transform: {x: 0, y: -4, size: 16}
      }));
    }, {
      classes: ['fa-leaflet-layer', 'drop-shadow']
    });
  };

  const attribution = 'Rendering <a href="https://geoinformatik.htw-dresden.de">Labor Geoinformatik (HTWD, Fak. GI)</a> | Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';

  export default {
    name: 'leaflet-map',
    props: {
      initialView: Object,
      memorials: Array,
    },
    mounted: function () {
      const vm = this;
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

      vm.map.on('moveend', () => {
        const {lat, lng} = vm.map.getCenter();
        vm.$emit('moveend', [lng, lat], vm.map.getZoom());
      });

      const scaleControl = L.control.scale();
      scaleControl.addTo(vm.map);

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
      initialView: function ({center, zoom}, oldView) {
        const vm = this;
        vm.map.flyTo(center, zoom);
      },
      memorials: function (newMemorials, oldMemorials) {
        const vm = this;
        const newMarkers = newMemorials.map(({position: [lng, lat], memorial_types, ...otherProps}) => {
          const memorialType = memorial_types[0].id;
          return L.marker([lat, lng], {
            icon: L.divIcon({
              className: 'fa-leaflet-icon',
              html: symbolLayer(memorialType).html,
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
