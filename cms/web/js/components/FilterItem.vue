<template>
  <li :class="['filter-item', {'active': enabled}, 'rounded']" v-on:click="onClick">
    <slot></slot>
  </li>
</template>

<script>
  export default {
    props: {
      id: [String, Number],
      title: String,
      enabled: {
        type: Boolean,
        default: false,
      },
      item: {
        type: Object,
        default() {
          return {};
        }
      },
    },
    methods: {
      onClick () {
        const vm = this;
        const event = vm.enabled ? 'disabled' : 'enabled';
        vm.$emit(event, vm.id);
      }
    }
  }
</script>

<style lang="scss">
  @import "../../scss/_variables";

  .filter-item {
    background-color: $gray-100;
    padding: 0 10px;
    margin: 3px;
    cursor: pointer;

    &.active {
      background-color: theme-color("primary");
      color: theme-color("light");

    }

    &:hover {
      box-shadow: 0 0 3px $gray-100;
    }

  }
</style>
