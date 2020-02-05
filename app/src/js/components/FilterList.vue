<template>
  <div class="filter-list">
    <span class="filter-list-heading d-flex justify-content-between mb-1">
      <span class="filter-list-heading-title text-muted">
        <slot name="header">{{ defaultHeader }}</slot>
      </span>
      <div class="btn-group" role="group" aria-label="Basic example">
        <button
          type="button"
          class="btn btn-sm btn-outline-secondary"
          :key="'btn-reset'"
          v-if="selection.size"
          v-on:click="resetFilter"
        >
          <i class="fas fa-fw fa-times"></i>
        </button>
        <button
          type="button"
          class="btn btn-sm btn-outline-secondary"
          :key="'btn-collapse'"
          v-if="collapsable && collapsed"
          v-on:click="collapsed = false"
        >
          <i class="fas fa-fw fa-eye-slash"></i>
        </button>
        <button
          type="button"
          class="btn btn-sm btn-outline-secondary"
          :key="'btn-show'"
          v-else-if="collapsable && !collapsed"
          v-on:click="collapsed = true"
        >
          <i class="fas fa-fw fa-eye"></i>
        </button>
      </div>
    </span>
    <div v-if="searchable && !collapsed" class="filter-list-search">
      <input
        type="text"
        class="form-control border-bottom-0 w-100"
        :placeholder="searchPlaceholder"
        v-model="searchTerm"
      />
    </div>
    <ul
      class="list-unstyled p-1 d-flex flex-wrap align-content-start"
      v-on:mouseover="hover = true"
      v-on:mouseleave="hover = false"
    >
      <filter-item
        v-for="item in visibleItems"
        :key="item.id"
        :id="item.id"
        :title="item.title"
        :enabled="selection.has(item.id)"
        v-on:enabled="enableFilter"
        v-on:disabled="disableFilter"
      >
        <template v-slot:default>
          <slot name="item" v-bind:item="item">{{item.title}}</slot>
        </template>
      </filter-item>
      <filter-item v-if="!items.length">
        <slot name="empty">{{ 'No filter item available.' | translate }}</slot>
      </filter-item>
      <filter-item
        v-else-if="!expanded && !visibleItems.length"
      >{{ 'No filter item selected.' | translate }}</filter-item>
    </ul>
  </div>
</template>

<script>
  import FilterItem from './FilterItem.vue';
  import translate from '../translate';

  const normalizeString = (str = '') => str.toLowerCase().trim();

export default {
  props: {
    items: {
      type: [Array, Set],
      default() {
        return [];
      }
    },

    toSearchableString: {
      type: Function,
      default: (x) => normalizeString(x.title)
    },

    selection: {
      type: Set,
      default() {
        return new Set();
      }
    },

    searchable: {
      type: Boolean,
      default: true
    },

    searchPlaceholder: {
      type: String,
      default: translate('Keyword..')
    },

    collapsable: {
      type: Boolean,
      default: true
    },

    initialCollapse: {
      type: Boolean,
      default: true
    }
  },
  components: {
    FilterItem
  },

  filters: {
    translate
  },

  data() {
    return {
      collapsed: true,
      hover: false,
      searchTerm: ''
    };
  },
  computed: {
    defaultHeader() {
      return `${this.selection.size} ${translate('items selected')}.`;
    },

    expanded() {
      if (this.collapsable) {
        return !this.collapsed || this.hover;
      } else {
        return true;
      }
    },

    visibleItems() {
      const vm = this;
      const selectedItems = vm.items.filter(x => vm.selection.has(x.id));

      if (!vm.expanded) return selectedItems;

      const normalizedSearchTerm = normalizeString(vm.searchTerm);
      const matchedItems = vm.items.filter(x => {
        const normalizedTitle = normalizeString(vm.toSearchableString(x));
        return (
          !vm.selection.has(x.id) &&
          normalizedTitle.indexOf(normalizedSearchTerm) > -1
        );
      });
      return selectedItems.concat(matchedItems);
    }
  },

  created() {
    this.collapsed = this.initialCollapse;
  },

  methods: {
    resetFilter() {
      this.$emit('change', new Set());
    },

    enableFilter(id) {
      const vm = this;
      const newSelection = new Set(vm.selection);
      newSelection.add(id);
      vm.$emit('change', newSelection);
    },

    disableFilter(id) {
      const vm = this;
      const newSelection = new Set(vm.selection);
      newSelection.delete(id);
      vm.$emit('change', newSelection);
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';

.filter-list {
  font-size: $font-size-sm;

  input {
    font-size: $font-size-sm;
  }

  ul {
    border: 1px solid theme-color('secondary');
    overflow: scroll;
    resize: vertical;
    max-height: 250px;
  }
}
</style>
