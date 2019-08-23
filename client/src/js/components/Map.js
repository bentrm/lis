import Vue from 'vue/dist/vue.esm';
import L from 'leaflet';
import 'leaflet.locatecontrol';
import 'leaflet.markercluster';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';


const template = `
  <div class="Map"></div>
`;

const Icon = L.Icon.extend({
  options: {
    iconUrl,
    iconRetinaUrl,
    shadowUrl,
    iconSize:    [25, 41],
    iconAnchor:  [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
    shadowSize:  [41, 41]
  },
});

const attribution = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';

Vue.component('leaflet-map', {
  props: ['currentSelection', 'memorials'],
  template,
  mounted: function() {
    const vm = this;
    const osmLayer = L.tileLayer(
      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      {attribution},
    );
    vm.clusterLayer = L.markerClusterGroup({
      polygonOptions: {
        color: '#69140e'
      },
      spiderLegPolylineOptions: {
        color: '#69140e'
      }
    });

    vm.map = L.map(vm.$el, {
      center: [50.7, 14.9],
      layers: [osmLayer, vm.clusterLayer],
      zoom: 8,
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
    currentSelection: function(newSelection, oldSelection) {
      const vm = this;

      if (newSelection) {
        const [lng, lat] = newSelection.position;
        const center = [lat, lng];
        vm.map.flyTo(center, 14);
      }
    },
    memorials: function(newMemorials, oldMemorials) {
      const vm = this;
      const newMarkers = newMemorials.map(memorial => {
        const [lng, lat] = memorial.position;
        return L.marker([lat, lng], {
          icon: new Icon,
          title: memorial.title
        });
      });

      vm.clusterLayer.clearLayers();
      vm.clusterLayer.addLayers(newMarkers);
    }
  }
});
