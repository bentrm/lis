<template>
  <span class="author-name">
      <span v-if="title && showDetails" class="title">{{ title }}</span>
      <span v-if="firstName" class="first-name text-muted">{{ firstName }}</span>
      <span v-if="lastName" class="last-name">{{ lastName }}</span>
      <span v-if="isPseudonym && showDetails" class="pseudonym">({{ 'pseudonym' | translate }})</span>
      <span v-if="birthName && showDetails" class="name-birth-name">({{ 'born' | translate }} {{ birthName }})</span>
  </span>
</template>

<script>
  import translate from '../translate';

  export default {
    props: {
      isPseudonym: Boolean,
      title: String,
      firstName: String,
      lastName: String,
      birthName: String,
      showDetails: {
        value: Boolean,
        default: false,
      }
    },
    filters: {
      translate
    },
    computed: {
      name() {
        const vm = this;
        return [vm.title, vm.first_name, vm.last_name].filter(x => x).join(' ');
      },
    }
  };
</script>

<style lang="scss">
</style>
