<template>
  <article class="mb-4">
    <template v-for="[heading, blocks] in content" v-if="blocks.length">
      <h4 :id="heading">{{ heading | humanize | capitalize | translate }}</h4>
      <paragraph
        v-for="block in blocks"
        :key="block.id"
        v-if="block.type === 'paragraph'"
        v-bind="block.value"></paragraph>
    </template>
  </article>
</template>

<script>
  import translate from '../translate';
  import {capitalize, humanize} from '../utils';
  import Paragraph from './Paragraph.vue';


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
    }
  };
</script>
