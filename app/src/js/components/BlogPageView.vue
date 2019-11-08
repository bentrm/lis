<template>
  <div class="container">
    <div class="row">
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
  </div>
</template>

<script>
import api from '../Api';
import translate from '../translate';
import Paragraph from './Paragraph.vue';
import FigureImage from './FigureImage.vue';

export default {
  props: {
    slug: String
  },

  components: {
    FigureImage,
    Paragraph
  },

  filters: {
    translate
  },

  data() {
    return {
      page: {}
    };
  },

  beforeRouteEnter(to, from, next) {
    api
      .getPage(to.params.slug || 'homepage')
      .then(json => next(vm => (vm.page = json)))
      .catch(response => next({ name: 'not-found' }));
  },
  // when route changes and this component is already rendered,
  // the logic will be slightly different.
  beforeRouteUpdate(to, from, next) {
    api
      .getPage(to.params.slug)
      .then(json => {
        this.page = json;
        next();
      })
      .catch(response => next({ name: 'not-found' }));
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';
</style>
