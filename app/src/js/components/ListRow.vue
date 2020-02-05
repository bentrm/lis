<template>
  <b-media tag="li" vertical-align="center" class="mb-2">
    <template v-slot:aside>
      <cms-image v-if="imgThumb" :src="imgThumb" :alt="imgTitle" :title="imgTitle" class="author-thumb border border-primary rounded-circle img-fluid"></cms-image>
      <b-img blank blank-color="grey" :width="25" :height="25" class="author-thumb border border-primary rounded-circle img-fluid" v-else></b-img>
    </template>

    <router-link :to="to">
      <slot></slot>
    </router-link>
  </b-media>
</template>

<script>
  import CmsImage from './CmsImage.vue';

  export default {
    props: {
      imgThumb: String,
      imgTitle: String,
      to: [Object, String],
    },

    components: {
      CmsImage
    },
  }
</script>
