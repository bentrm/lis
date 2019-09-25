<template>
  <div class="filter-list">
    <div class="filter-list-heading">
      <span>{{ title }} ({{selection.size}}/{{items.length}})</span>
      <span v-if="selection.size" v-on:click="onClear"><i class="fas fa-times"></i></span>
    </div>
    <ul class="list-unstyled">
      <li v-for="item in items"
          :key="item.id"
          :class="{'active': selection.has(item.id)}"
          v-on:click="onClick(item)"
      >
        {{ item.title }} <span v-if="selection.has(item.id)"><i class="fas fa-times"></i></span>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    props: {
      title: String,
      items: {
        type: Array,
        default () {
          return [];
        }
      },
      selection: {
        type: Set,
        default () {
          return new Set;
        }
      },
    },
    methods: {
      onClear () {
        this.$emit('change', new Set());
      },

      onClick (item) {
        const vm = this;
        const id = item.id;
        const currentSet = new Set(vm.selection);

        if (currentSet.has(id)) {
          currentSet.delete(id);
        } else {
          currentSet.add(id);
        }

        vm.$emit('change', currentSet);
      }
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
      max-height: 8rem;
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
