<template>
  <figure class="user-image figure d-flex flex-column align-items-center">
    <img
      :src="src"
      :alt="alt"
      :title="label"
      v-on:click="modalOpen = !!srcModal"
      class="preview figure-img img-fluid shadow">
    <figcaption
      class="figure-caption small d-none d-md-block text-center p-1"
      v-if="caption"
      v-text="caption">
    </figcaption>

    <b-modal :title="title" size="lg" title-tag="b" :ok-only="true" v-model="modalOpen">
      <div class="col-12 align-content-center">
        <figure
          class="figure d-flex flex-column align-items-center">
          <img
            :src="srcModal"
            :alt="alt"
            :title="label"
            class="figure-img img-fluid shadow">
          <figcaption
            class="figure-caption text-center p-1"
            v-if="captionModal || caption"
            v-text="captionModal || caption">
          </figcaption>
          <figcaption
            class="figure-caption text-center p-1"
            v-if="copyrightLabel"
            v-text="copyrightLabel">
          </figcaption>
        </figure>
      </div>
    </b-modal>

  </figure>
</template>

<script>
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
    },

    data() {
      return {
        modalOpen: false
      };
    },

    computed: {
      copyrightLabel () {
        const value = '';
        if (this.copyright) {
          return `© ${this.copyright}`;
        }
        return value;
      },

      label () {
        let value = this.title;

        if (this.copyrightLabel) {
          value += ` (${this.copyrightLabel})`;
        }
        return value
      }
    }
  };
</script>

<style lang="scss">
  .user-image {
    .preview {
      cursor: pointer;
    }

    .modal-body img {
      max-height: 60vh;
    }
  }
</style>
