<template>
  <img
    :src="src"
    :alt="alt"
    :title="label"
    class="border border-primary">
</template>

<script>
  export default {
    props: {
      src: String,
      alt: String,
      title: String,
      copyright: String,
    },

    computed: {
      label () {
        let value = this.title;

        if (this.copyright) {
          value += ` (© ${this.copyright})`;
        }
        return value
      }
    }
  };
</script>
