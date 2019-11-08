<template>
  <img :src="absSrc" :alt="alt" :title="title" />
</template>

<script>
import { cmsHost } from '../config';

export default {
  props: {
    src: String,
    alt: String,
    title: String
  },
  computed: {
    absSrc() {
      return cmsHost + this.src;
    }
  }
};
</script>

<style lang="scss">
</style>
