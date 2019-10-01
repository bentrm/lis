<template lang="html">
  <div class="Author-card media">
    <img
      v-if="image"
      :src="image.thumb"
      :alt="image.title"
      :title="image.title"
      class="border border-primary rounded-circle align-self-baseline">
    <span v-else class="placeholder"></span>
    <div class="media-body ml-4">
      <p class="p-0 h4">
        <a :href="url">
          <span v-if="first_name" class="small text-muted">{{ first_name }}</span>
          {{ last_name }}
        </a>
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      image: Object,
      url: String,
      academic_title: String,
      first_name: String,
      last_name: String,
      birth_name: String,
    }
  };
</script>

<style lang="scss">
  @import '../../scss/variables';

  .Author-card {
    img {
      height: 30px;
      width: 30px;
      margin-bottom: $paragraph-margin-bottom;
    }

    .placeholder {
      width: 30px;
    }
  }
</style>
