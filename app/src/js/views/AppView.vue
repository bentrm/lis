<template>
  <app-layout />
</template>

<script>
  import translate, {getCurrentLanguage} from '../translate';
  import AppLayout from '../components/AppLayout.vue';

  export default {
  components: {
    AppLayout,
  },

  filters: {
    translate
  },

  metaInfo() {
    return {
      title: translate('Home'),
      titleTemplate: `%s | ${translate('Literary landscape')}`,
      htmlAttrs: {
        lang: getCurrentLanguage(),
      }
    };
  },
};
</script>

<style lang="scss">
@import 'src/scss/main';
</style>
