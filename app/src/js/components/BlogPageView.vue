<template>
  <div class="container">
    <div class="row" v-if="!error">
      <div class="col-12">
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
              :caption="value.caption"
              :copyright="value.copyright"
              class="figure d-block text-center"
            ></figure-image>
          </template>
        </article>
      </div>
    </div>
    <div class="row" v-else>
      <div class="col">
        <h1 class="mt-4">404: {{ 'Page not found.' | translate }}</h1>
        <p>
          <router-link :to="{name: 'index'}">{{ 'Back to homepage.' | translate }}</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../state/store';
import { fetchPage } from '../state/actions';
import translate from '../translate';
import Paragraph from './Paragraph.vue';
import FigureImage from './FigureImage.vue';

export default {
  components: {
    FigureImage,
    Paragraph
  },

  filters: {
    translate
  },

  computed: {
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
@import '../../scss/variables';
</style>
