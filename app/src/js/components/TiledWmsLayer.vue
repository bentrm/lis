<script>
import TileLayer from 'vue2-leaflet/src/mixins/TileLayer';
import {
  optionsMerger,
  propsBinder,
  findRealParent
} from 'vue2-leaflet/src/utils/utils.js';
import Options from 'vue2-leaflet/src/mixins/Options.js';
import { tileLayer, DomEvent } from 'leaflet';

const TiledWmsLayerMixin = {
  mixins: [TileLayer],
  props: {
    layers: {
      type: String,
      default: ''
    },
    styles: {
      type: String,
      default: ''
    },
    format: {
      type: String,
      default: 'image/jpeg'
    },
    format_options: {
      type: String,
      default: 'dpi:90'
    },
    tiled: {
      type: Boolean,
      default: true
    },
    transparent: {
      type: Boolean,
      custom: false
    },
    version: {
      type: String,
      default: '1.1.1'
    },
    crs: {
      default: null
    },
    upperCase: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    this.tileLayerWMSOptions = {
      ...this.tileLayerOptions,
      layers: this.layers,
      styles: this.styles,
      format: this.format,
      format_options: this.format_options,
      tiled: this.tiled,
      transparent: this.transparent,
      version: this.version,
      crs: this.crs,
      upperCase: this.upperCase
    };
  }
};

export default {
  mixins: [TiledWmsLayerMixin, Options],
  props: {
    baseUrl: {
      type: String,
      default: null
    }
  },
  mounted() {
    const options = optionsMerger(this.tileLayerWMSOptions, this);
    this.mapObject = tileLayer.wms(this.baseUrl, options);
    DomEvent.on(this.mapObject, this.$listeners);
    propsBinder(this, this.mapObject, this.$options.props);
    this.parentContainer = findRealParent(this.$parent);
    this.parentContainer.addLayer(this, !this.visible);
    this.$nextTick(() => {
      this.$emit('ready', this.mapObject);
    });
  }
};
</script>
