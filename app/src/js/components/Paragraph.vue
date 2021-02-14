<template>
  <div class="paragraph">
    <h5 v-if="heading">
      <a v-if="document.url"
         :href="document.url"
         :alt="document.title"
      >
        <i class="fas fa-file"></i>
        {{ heading }}
      </a>
      <span v-else>{{ heading }}</span>
    </h5>

    <div v-if="images.length" class="row">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="col-12 col-xs-6 col-sm-4 col-md-3 justify-content-center align-items-center"
      >
        <figure-image
          :thumb="true"
          :src="image.small"
          :src-modal="image.large"
          :alt="image.title"
          :title="image.title"
          :caption="image.caption"
          :copyright="image.copyright"
          v-on:click="currentImage = image.id"
        ></figure-image>
      </div>
    </div>

    <div class="text-muted" v-if="document && document.copyright">© {{ document.copyright }}</div>
    <div v-html="parsedContent" ref="content"></div>

    <div v-if="footnotes.length">
      <h6>{{ 'References' | translate }}</h6>
      <footer class="footnotes">
        <ol>
          <footnote
            v-for="(footnote, index) in footnotes"
            :key="index"
            :tag="footnote.tag"
            :content="footnote.footnote"
          ></footnote>
        </ol>
      </footer>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue/dist/vue.esm';
  import Bookmark from './Bookmark.vue';
  import Footnote from './Footnote.vue';
  import FigureImage from './FigureImage.vue';
  import translate from '../translate';

  const BookmarkComponent = Vue.extend(Bookmark);

export default {
  props: {
    heading: {
      type: String,
      default: ''
    },
    images: {
      type: Array,
      default() {
        return [];
      }
    },
    document: {
      type: Object,
    },
    content: {
      type: String,
      default: ''
    },
    footnotes: {
      type: Array,
      default() {
        return [];
      }
    },
    editor: String
  },
  components: {
    Footnote,
    FigureImage
  },

  filters: {
    translate
  },

  data() {
    return {
      currentImage: null
    };
  },

  computed: {
    dict() {
      return this.footnotes.reduce((acc, cur, index) => {
        acc[cur.tag.toString()] = [index, cur];
        return acc;
      }, {});
    },

    parsedContent() {
      return this.content.replace(/\[([a-zA-Z0-9]*)]/g, '<span class="footnote">$1</span>');
    }
  },

  mounted() {
    const vm = this;

    vm.$nextTick(() => {
      const contentEl = vm.$refs['content'];

      contentEl.querySelectorAll('blockquote').forEach(node => {
        node.className = node.className + ' blockquote text-right';
      });

      contentEl.querySelectorAll('span.footnote').forEach(node => {
        const tag = node.textContent;
        if (!this.dict.hasOwnProperty(tag)) {
          console.warn(`Footnote tagged ${tag} not found.`, node);
          return;
        }

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
};
</script>

<style lang="scss">
@import '../../scss/variables';

.paragraph {
  p {
    hyphens: auto;
  }

  footer.footnotes {
    font-size: .8rem;

    li {
      padding: .2rem 0;
    }

    li.active {
      background-color: gray("200");
    }

    p {
      margin-bottom: 0;
    }
  }
}
</style>
