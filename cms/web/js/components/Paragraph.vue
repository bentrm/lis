<template>
  <div class="struct-paragraph">
    <h5 v-if="heading">{{ heading }}</h5>
    <div v-html="content" ref="content"></div>
    <footer v-if="footnotes.length" class="footnotes">
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
  import Footnote from './Footnote.vue';
  import Bookmark from './Bookmark.vue';

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
          const bookmark = new BookmarkComponent();

          bookmark.$slots.default = [index + 1];
          bookmark.$mount();
          node.replaceWith(bookmark.$el);

          // $(bookmark.$el).popover({
          //   content: $(footnote.footnote).html(),
          //   delay: {show: 500, hide: 1000}
          // });
        });
      });

    }
  }
</script>

<style lang="scss">
  .rich-text p {
    hyphens: auto;
  }

  .footnotes p {
    margin-bottom: .5rem;
  }

</style>
