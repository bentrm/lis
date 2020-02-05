<template>
  <b-media
    tag="li"
    vertical-align="center"
    class="mb-2"
  >
    <template v-slot:aside>
      <cms-image
        v-if="author.title_image"
        :src="author.title_image.thumb"
        :alt="author.title_image.title"
        :title="author.title_image.title"
        class="author-thumb border border-primary rounded-circle img-fluid"
      ></cms-image>
      <b-img
        blank
        blank-color="grey"
        :width="25"
        :height="25"
        class="author-thumb border border-primary rounded-circle img-fluid"
        v-else
      ></b-img>
    </template>

    <router-link
      :to="{name: 'author-detail', params: { slug: author.slug, level: 'discover' }}"
    >
      <author-name
        :show-details="false"
        :isPseudonym="name.is_pseudonym"
        :title="name.title"
        :firstName="name.first_name"
        :lastName="name.last_name"
        :birthName="name.birth_name" />
    </router-link>
  </b-media>
</template>

<script>
  import CmsImage from './CmsImage.vue';
  import AuthorName from './AuthorName.vue';

  export default {
    props: {
      author: Object,
    },

    components: {
      AuthorName,
      CmsImage
    },

    computed: {
      name() {
        const vm = this;
        return vm.author.also_known_as[0];
      }
    }
  }
</script>
