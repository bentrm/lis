<template>
  <li v-html="content"></li>
</template>

<script>
  export default {
    props: {
      tag: String,
      content: String
    }
  }
</script>
