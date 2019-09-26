<template>
  <div class="filter-list">
    <div class="filter-list-heading">
      <slot name="header">
        <span v-if="selection.size">
          {{selection.size}} filters selected.
        </span>
        <span v-else>
          No filters selected.
        </span>
      </slot>
      <span v-if="selection.size" v-on:click="resetFilter">
        <i class="fas fa-times"></i>
      </span>
    </div>
    <ul class="list-unstyled">
      <filter-item
        v-for="item in items"
        :key="item.id"
        :item="item"
        :enabled="selection.has(item.id)"
        v-on:enabled="enableFilter"
        v-on:disabled="disableFilter"
      >
        <template v-slot:default>
          <slot name="item" v-bind:item="item">
            {{item.title}}
          </slot>
        </template>
      </filter-item>
        <li v-if="!items.length">
          <slot name="empty">
            No filters available.
          </slot>
        </li>
    </ul>
  </div>
</template>

<script>
  import FilterItem from './FilterItem.vue';

  export default {
    props: {
      items: {
        type: [Array, Set],
        default () {
          return [];
        }
      },
      selection: {
        type: Set,
        default () {
          return new Set();
        }
      }
    },
    components: {
      FilterItem,
    },
    methods: {
      resetFilter() {
        this.$emit('change', new Set());
      },

      enableFilter (item) {
        const vm = this;
        const newSelection = new Set(vm.selection);
        newSelection.add(item.id);
        vm.$emit('change', newSelection);
      },

      disableFilter (item) {
        const vm = this;
        const newSelection = new Set(vm.selection);
        newSelection.delete(item.id);
        vm.$emit('change', newSelection);
      },
    }
  }
</script>

<style lang="scss">
  @import "../../scss/variables";

  .filter-list {
    .filter-list-heading {
      margin-bottom: 0;
    }

    ul {
      border: 1px solid theme-color("secondary");
      font-size: .8rem;
      height: 8rem;
      overflow: scroll;

      li {
        padding: 0 10px;

        &.active {
          background-color: $gray-600;
          color: theme-color("light");
        }
      }
    }
  }
</style>
