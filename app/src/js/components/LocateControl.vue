<template>
  <div style="display: none;">
    <slot v-if="ready"></slot>
  </div>
</template>

<script>
import { DomEvent } from 'leaflet';
import { findRealParent, propsBinder } from 'vue2-leaflet';
import LocateControl from '../leaflet.locatecontrol';

const props = {
  options: {
    type: Object,
    default() {
      return {};
    }
  },
  visible: {
    type: Boolean,
    custom: true,
    default: true
  }
};
export default {
  props: props,
  data() {
    return {
      ready: false
    };
  },
  beforeDestroy() {
    this.parentContainer.removeLayer(this);
  },
  mounted() {
    this.mapObject = new LocateControl(this.options);
    DomEvent.on(this.mapObject, this.$listeners);
    propsBinder(this, this.mapObject, props);
    this.ready = true;
    this.parentContainer = findRealParent(this.$parent);
    this.mapObject.addTo(this.parentContainer.mapObject, !this.visible);
  }
};
</script>

<style>
@import '~leaflet.locatecontrol/dist/L.Control.Locate.css';
</style>
