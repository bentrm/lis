<template>
  <figure class="figure-image figure d-flex flex-column align-items-center">
    <cms-image
      :src="src"
      :alt="alt + copyrightSuffix"
      :title="title + copyrightSuffix"
      v-b-modal="modalId"
      class="preview figure-img img-fluid"
      :class="{'has-modal': srcModal, 'img-thumbnail': thumb}"
    />
    <figcaption
      :id="figcaptionId"
      class="figure-caption d-block small text-center p-1"
      :aria-label="figcaption"
      v-if="figcaption"
      v-text="figcaption.length > 100 ? figcaption.substring(0, 100) + '...' : figcaption"
    />
    <b-popover :target="figcaptionId" triggers="hover" v-if="figcaption.length > 100">
      {{ figcaption }}
    </b-popover>

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
    copyright: String,
    thumb: {
      type: Boolean,
      default: false
    },
  },

  components: {
    CmsImage
  },

  data() {
    const currentId = id++;
    return {
      figcaptionId: `figure-image-caption-${currentId}`,
      modalId: `figure-image-modal-${currentId}`
    };
  },

  computed: {
    copyrightSuffix() {
      let value = "";
      if (this.copyright) {
        value += ` (©${this.copyright})`;
      }
      return value;
    },
    figcaption() {
      let value = (this.caption || this.title);
      if (this.copyright) {
        value += ` (©${this.copyright})`;
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
