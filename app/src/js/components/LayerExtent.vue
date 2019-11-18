<template>
  <div style="display: none;">
    <slot v-if="ready"></slot>
  </div>
</template>

<script>
import ExtentControl from '../leaflet.extentcontrol';
import { findRealParent, propsBinder } from 'vue2-leaflet';
import { DomEvent } from 'leaflet';

export default {
  props: {
    layer: Object
  },
  data() {
    return {
      ready: false
    };
  },
  watch: {
    layer(newLayer) {
      this.mapObject.setLayer(newLayer);
    }
  },
  mounted() {
    this.mapObject = new ExtentControl(this.options);
    DomEvent.on(this.mapObject, this.$listeners);
    propsBinder(this, this.mapObject, this.props);
    this.ready = true;
    this.parentContainer = findRealParent(this.$parent);
    this.mapObject.addTo(this.parentContainer.mapObject);
  }
};
</script>
