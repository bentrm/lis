<template>
  <figure class="figure-image figure d-flex flex-column align-items-center">
    <cms-image
      :src="src"
      :alt="alt"
      :title="label"
      v-on:click.native="e => srcModal && onThumbnailClick()"
      class="preview figure-img img-fluid"
      :class="{'has-modal': srcModal}"
    />
    <figcaption
      class="figure-caption d-block small text-center p-1"
      v-if="caption"
      v-text="caption"
    ></figcaption>

    <b-modal :title="title" size="lg" title-tag="b" :ok-only="true" v-model="modalOpen">
      <div class="col-12 align-content-center">
        <figure class="figure d-flex flex-column align-items-center">
          <cms-image :src="srcModal" :alt="alt" :title="label" class="figure-img img-fluid"></cms-image>
          <figcaption
            class="figure-caption text-center p-1"
            v-if="captionModal || caption"
            v-text="captionModal || caption"
          ></figcaption>
          <figcaption
            class="figure-caption text-center p-1"
            v-if="copyrightLabel"
            v-text="copyrightLabel"
          ></figcaption>
        </figure>
      </div>
    </b-modal>
  </figure>
</template>

<script>
import CmsImage from './CmsImage.vue';

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
      modalOpen: false
    };
  },

  computed: {
    copyrightLabel() {
      const value = '';
      if (this.copyright) {
        return `© ${this.copyright}`;
      }
      return value;
    },

    label() {
      let value = this.title;

      if (this.copyrightLabel) {
        value += ` (${this.copyrightLabel})`;
      }
      return value;
    }
  },

  methods: {
    onThumbnailClick() {
      this.modalOpen = !!this.srcModal;
    }
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
