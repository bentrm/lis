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
  import api from '../Api';
  import translate from '../translate';
  import FigureImage from './FigureImage.vue';
  import Paragraph from './Paragraph.vue';


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
      error: false,
      page: {}
    };
  },

  beforeRouteEnter(to, from, next) {
    api
      .getPage(to.params.slug || 'homepage')
      .then(json => {
        next(vm => {
          vm.page = json;
          vm.error = false;
        })
      })
      .catch(() => {
        next(vm => {
          vm.error = true
        })
      });
  },
  // when route changes and this component is already rendered,
  // the logic will be slightly different.
  beforeRouteUpdate(to, from, next) {
    const vm = this;
    api
      .getPage(to.params.slug)
      .then(json => {
        vm.page = json;
        vm.error = false;
        next();
      })
      .catch(() => next(vm => vm.error = true));
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';
</style>
