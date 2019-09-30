<template>
  <div class="card memorial-card">
    <span class="close" v-on:click="$emit('hide')">
          <i class="fas fa-times"></i>
        </span>
    <img
      class="card-img-top"
      v-if="banner"
      :src="banner"
      :alt="title">
    <div class="card-body">
      <h5>{{ title }}</h5>
      <ul class="list-unstyled">
        <li v-for="author in authors" :key="author.id">
          <a :href="author.url">{{author.first_name}} {{author.last_name}}</a>
        </li>
      </ul>
      <div v-if="introduction" v-html="introduction"></div>
      <address class="address" v-if="address" v-html="address"></address>
      <div v-if="contactInfo" v-html="contactInfo"></div>
      <div v-if="directions" v-html="directions"></div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      banner: String,
      title: String,
      authors: Array,
      address: String,
      contactInfo: String,
      directions: String,
      introduction: String
    },
  };
</script>

<style lang="scss">
  .memorial-card {
    .close {
      color: white;
      position: absolute;
      top: 10px;
      right: 10px;
    }
  }
</style>
