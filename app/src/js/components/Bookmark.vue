<template>
  <span class="bookmark-wrapper">
    <span
      :id="bookmarkId"
      class="bookmark fa-layers fa-fw"
      ref="bookmark"
    >
      <i class="fas fa-bookmark"></i>
      <span class="fa-layers-text fa-inverse" data-fa-transform="shrink-5 up-2" v-text="index"></span>
    </span>
    <b-popover
      :target="bookmarkId"
      triggers="hover focus">
      <div v-html="content"></div>
    </b-popover>
  </span>
</template>

<script>
  let _id = 0;

  export default {
    props: {
      index: Number,
      content: String,
    },

    data() {
      return {
        bookmarkId: (++_id) + '-bookmark'
      };
    }
  }
</script>

<style lang="scss">
  @import '../../scss/variables';

  .bookmark-wrapper {
    white-space: nowrap;
  }

  .bookmark {
    color: theme-color('primary');
  }
</style>
