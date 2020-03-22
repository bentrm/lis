<template>
  <div style="display: none;">
    <slot v-if="ready"></slot>
  </div>
</template>

<script>
  import ExtentControl from '../leaflet.extentcontrol';
  import {findRealParent, propsBinder} from 'vue2-leaflet';
  import {DomEvent} from 'leaflet';

  export default {
    props: {
      extent: Array,
    },
    data() {
      return {
        ready: false
      };
    },

    watch: {
      extent(newExtent) {
        this.mapObject.setExtent(newExtent);
      }
    },
    mounted() {
      const vm = this;
      vm.mapObject = new ExtentControl(vm.options);
      DomEvent.on(vm.mapObject, vm.$listeners);
      propsBinder(vm, vm.mapObject, vm.props);
      vm.ready = true;
      vm.parentContainer = findRealParent(vm.$parent);
      vm.mapObject.addTo(this.parentContainer.mapObject);

      vm.mapObject.setExtent(vm.extent);
    }
  };
</script>
