<template>
  <div class="Author-list">
    <ul class="list-unstyled" id="author-list">
      <author-list-row v-for="author in authors" :key="author.id" :author="author"/>
    </ul>

    <b-pagination
      aria-controls="#author-list"
      align="center"
      v-if="totalPages > 1"
      v-model="page"
      :total-rows="count"
      v-on:change="e => $emit('change', e)" />
  </div>
</template>

<script>
  import translate from '../translate';
  import AuthorListRow from '../components/AuthorListRow.vue';

  export default {
    components: {
      AuthorListRow
    },

    props: {
      authors: {
        type: Array,
        default: [],
      },
      page: Number,
      count: Number,
      totalPages: Number,
      setPage: Function,
    },

    filters: {
      translate,
    }
  };
</script>

<style lang="scss">
  @import 'src/scss/variables';

  .Author-list ul {
    column-rule: 1px solid theme-color("primary");

    .author-thumb {
      max-height: 25px;
    }
  }

  @media (min-width: map_get($grid-breakpoints, "lg")) {
    .Author-list ul {
      column-count: 2;
    }
  }
</style>
