<template>
  <figure class="figure-image figure d-flex flex-column align-items-center">
    <cms-image
      :src="src"
      :alt="alt + copyrightSuffix"
      :title="title + copyrightSuffix"
      v-b-modal="modalId"
      class="preview figure-img img-fluid"
      :class="{'has-modal': srcModal}"
    />
    <figcaption
      class="figure-caption d-block small text-center p-1"
      v-if="caption || title"
      v-text="(caption || title) + copyrightSuffix"
    ></figcaption>

    <b-modal :id="modalId" :title="title" size="lg" title-tag="b" :ok-only="true">
      <div class="col-12 align-content-center">
        <figure class="figure d-flex flex-column align-items-center">
          <cms-image :src="srcModal" :alt="alt + copyrightSuffix" :title="title + copyrightSuffix" class="figure-img img-fluid"></cms-image>
          <figcaption
            class="figure-caption text-center p-1"
            v-if="captionModal || caption || title"
            v-text="(captionModal || caption || title) + copyrightSuffix"
          ></figcaption>
        </figure>
      </div>
    </b-modal>
  </figure>
</template>

<script>
import CmsImage from './CmsImage.vue';

let id = 0;

export default {
  props: {
    src: String,
    srcModal: {
      type: String,
      default: ''
    },
    alt: String,
    title: String,
    caption: String,
    captionModal: String,
    copyright: String
  },

  components: {
    CmsImage
  },

  data() {
    return {
      modalId: `figure-image-modal-${id++}`
    };
  },

  computed: {
    copyrightSuffix() {
      const value = '';
      if (this.copyright) {
        return ` (© ${this.copyright})`;
      }
      return value;
    },
  }
};
</script>

<style lang="scss">
.figure-image {
  .preview.has-modal {
    cursor: pointer;
  }

  .modal-body img {
    max-height: 60vh;
  }
}
</style>
