<template>
  <div class="container">
    <div class="row">
      <div v-if="!error" class="col-12">
        <h1 class="mt-4">{{ page.title }}</h1>

        <article>
          <template v-for="{id, type, value} in page.body">
            <h2
              v-if="type === 'heading'"
              :key="id"
            >
              {{ value }}
            </h2>

            <div
              v-else-if="type ==='paragraph'"
              :key="id"
              v-html="value"></div>

            <figure
              v-else-if="type === 'image'"
              :key="id"
              class="figure d-block text-center"
            >
              <img
                :src="value.mid"
                :alt="value.title"
                class="figure-img img-fluid rounded">
              <figcaption class="figure-caption">
                {{ value.caption }}
              </figcaption>
            </figure>
          </template>
        </article>
      </div>
      <div v-else class="col-12">
        <h1 class="mt-4">
          {{ 'Error' | translate }} {{ error.status }}: {{ error.statusText | translate }}
        </h1>
        <p>
          <router-link
            class="navbar-brand"
            :to="{name: 'blog-page'}"
          >
            {{ 'Back to homepage.' | translate }}
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '../Api';
  import translate from '../translate';
  import Paragraph from './Paragraph.vue';


  export default {

    props: {
      slug: String
    },

    components: {
      Paragraph,
    },

    filters: {
      translate,
    },

    data() {
      return {
        page: {
          body: []
        },
        error: null,
      }
    },

    created () {
      this.fetchPage(this.slug);
    },

    watch: {
      '$route' () {
        this.fetchPage(this.slug);
      }
    },

    methods: {
      fetchPage (slug) {
        const vm = this;
        api
          .getPage(slug)
          .then(json => {
            vm.error = null;
            vm.page = json;
          })
          .catch(response => vm.error = response);
      }
    }
  }

</script>

<style lang="scss">
  @import '../../scss/variables';


</style>
