<template>
  <cms-image :src="src" :alt="alt" :title="label" class="border border-primary" />
</template>

<script>
import CmsImage from './CmsImage.vue';

export default {
  props: {
    src: String,
    alt: String,
    title: String,
    copyright: String
  },

  components: {
    CmsImage
  },

  computed: {
    label() {
      let value = this.title;

      if (this.copyright) {
        value += ` (© ${this.copyright})`;
      }
      return value;
    }
  }
};
</script>
