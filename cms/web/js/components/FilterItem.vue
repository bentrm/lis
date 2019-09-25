<template>
  <li :class="{'active': enabled}" v-on:click="onClick">
    <slot></slot>
    <span v-if="enabled">
      <i class="fas fa-times"></i>
    </span>
  </li>
</template>

<script>
  export default {
    props: {
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
        vm.$emit(event, vm.item);
      }
    }
  }
</script>
