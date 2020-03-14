<template>
  <article class="mb-4">
    <template v-for="[heading, blocks] in content" v-if="blocks.length">
      <h4 :id="heading">{{ heading | humanize | capitalize | translate }}</h4>
      <paragraph
        v-for="block in blocks"
        :key="block.id"
        v-if="block.type === 'paragraph' || block.type === 'material'"
        v-bind="block.value"></paragraph>
    </template>
  </article>
</template>

<script>
  import AnchorJS from 'anchor-js/anchor';
  import translate from '../translate';
  import {capitalize, humanize} from '../utils';
  import Paragraph from './Paragraph.vue';

  const headingAnchors = new AnchorJS({
    icon: '¶'
  });
  const paragraphAnchors = new AnchorJS({
    placement: 'left',
    icon: '¶'
  });

  export default {
    props: {
      content: {
        type: Array,
        default: []
      },
    },

    components: {
      Paragraph,
    },

    filters: {
      capitalize,
      humanize,
      translate
    },

    mounted() {
      this.$nextTick(() => {
        headingAnchors
          .add('article h1')
          .add('article h2')
          .add('article h3')
          .add('article h4')
          .add('article h5')
          .add('article h6');
        paragraphAnchors.add('.paragraph > div > p')
      })
    }
  };
</script>
