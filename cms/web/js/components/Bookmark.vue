<template>
  <span class="bookmark fa-layers fa-fw mr-1">
    <i class="fas fa-bookmark"></i>
    <span class="fa-layers-text fa-inverse" data-fa-transform="shrink-5 up-2">
      <slot></slot>
    </span>
  </span>
</template>

<script>
  export default {
    props: {
      index: Number
    }
  }
</script>

<style lang="scss">
  @import '../../scss/variables';

  .bookmark {
    color: theme-color('primary');
  }
</style>
