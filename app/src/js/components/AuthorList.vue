<template>
  <div class="Author-list">
    <ul class="list-unstyled">
      <author-list-row v-for="author in authors" :key="author.id" :author="author"/>
    </ul>

    <pagination
      v-if="totalPages > 1"
      :currentPage="page"
      :totalPages="totalPages"
      v-on:change="e => $emit('change', e)">
    </pagination>
  </div>
</template>

<script>
  import translate from '../translate';
  import Pagination from '../components/Pagination.vue';
  import AuthorListRow from '../components/AuthorListRow.vue';

  export default {
    components: {
      AuthorListRow,
      Pagination,
    },

    props: {
      authors: {
        type: Array,
        default: [],
      },
      page: Number,
      totalPages: Number,
      setPage: Function,
    },

    filters: {
      translate,
    },

    methods: {
      onChange(event) {
        const vm = this;
        vm.onChange(event)
      }
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
