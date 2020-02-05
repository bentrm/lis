<template>
  <page-layout>
    <div v-if="!error">
      <h1 class="mt-4">{{ page.title }}</h1>

      <article>
        <template v-for="{id, type, value} in page.body">
          <h2 v-if="type === 'heading'" :key="id">{{ value }}</h2>

          <div v-else-if="type ==='paragraph'" :key="id" v-html="value"></div>

          <figure-image
            v-else-if="type === 'image'"
            :key="id"
            :src="value.mid"
            :src-modal="value.large"
            :alt="value.title"
            :title="value.title"
            :caption="value.caption"
            :copyright="value.copyright"
            class="figure d-block text-center"
          ></figure-image>
        </template>
      </article>
    </div>
    <error-fallback v-else></error-fallback>
  </page-layout>
</template>

<script>
  import store from '../state/store';
  import {fetchPage} from '../state/actions';
  import translate from '../translate';
  import Paragraph from '../components/Paragraph.vue';
  import FigureImage from '../components/FigureImage.vue';
  import ErrorFallback from '../components/ErrorFallback.vue';
  import PageLayout from '../components/PageLayout.vue';

  export default {
  components: {
    ErrorFallback,
    FigureImage,
    Paragraph,
    PageLayout,
  },

  filters: {
    translate
  },

  metaInfo() {
    let title = 'LIS - Blog';
    if (this.$store.state.page.current) {
      title = this.$store.state.page.current.title;
    }
    return {
      title,
    };
  },

  computed: {
    error() {
      return this.$store.state.page.error;
    },

    page() {
      return this.$store.state.page.current;
    }
  },

  beforeRouteEnter(to, from, next) {
    const slug = to.params.slug || 'homepage';
    store.dispatch(fetchPage, { slug }).then(() => next());
  },

  beforeRouteUpdate(to, from, next) {
    const slug = to.params.slug || 'homepage';
    store.dispatch(fetchPage, { slug }).then(() => next());
  }
};
</script>

<style lang="scss">
@import 'src/scss/variables';
</style>
