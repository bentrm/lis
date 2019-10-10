<template>
  <div class="paragraph">
    <h5 v-if="heading">{{ heading }}</h5>

    <div v-if="images.length" class="row">
      <div
        v-for="image in images"
        class="col-12 col-xs-6 col-sm-4 col-md-3 justify-content-center align-items-center"
      >
        <user-image
          :src="image.small"
          :src-modal="image.large"
          :alt="image.title"
          :title="image.title"
          :caption="image.caption"
          :copyright="image.copyright"
          v-on:click="currentImage = image.id"
        ></user-image>

      </div>
    </div>

    <div v-html="content" ref="content"></div>

    <footer v-if="footnotes.length">
      <ol class="border-left">
        <footnote
          v-for="(footnote, index) in footnotes"
          :key="index"
          :tag="footnote.tag"
          :content="footnote.footnote"></footnote>
      </ol>
    </footer>
  </div>
</template>

<script>
  import Vue from 'vue/dist/vue.esm';
  import Bookmark from './Bookmark.vue';
  import Footnote from './Footnote.vue';
  import UserImage from './UserImage.vue';


  const BookmarkComponent = Vue.extend(Bookmark);

  export default {
    props: {
      heading: {
        type: String,
        default: ''
      },
      images: {
        type: Array,
        default () {
          return [];
        }
      },
      content: {
        type: String,
        default: ''
      },
      footnotes: {
        type: Array,
        default () {
          return [];
        }
      },
      editor: String
    },
    components: {
      Footnote,
      UserImage,
    },

    data () {
      return {
        currentImage: null,
      }
    },

    computed: {
      dict () {
        return this.footnotes.reduce((acc, cur, index) => {
          acc[cur.tag.toString()] = [index, cur];
          return acc;
        }, {});
      }
    },

    mounted () {
      const vm = this;

      vm.$nextTick(() => {
        vm.$refs['content'].querySelectorAll('span.footnote').forEach(node => {
          const tag = node.textContent;
          const [index, footnote] = this.dict[tag];

          const bookmark = new BookmarkComponent({
            propsData: {
              index: index + 1,
              content: footnote.footnote
            }
          });
          bookmark.$mount();
          node.replaceWith(bookmark.$el);
        });
      });

    }
  }
</script>

<style lang="scss">
  @import '../../scss/variables';

  .paragraph {

    p {
      hyphens: auto;
    }

    footer {
      font-size: $font-size-sm;

      p {
        margin-bottom: .5rem;
      }
    }
  }
</style>
