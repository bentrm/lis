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
      <b>{{ 'GPS Position' | translate}}: {{ position[0] | round }}, {{ position[1] | round }}</b>
      <div v-if="introduction" v-html="introduction"></div>
      <template v-if="address">
        <b>{{ 'Address' | translate }}:</b>
        <address v-html="address"></address>
      </template>
      <template v-if="contactInfo">
        <b>{{ 'Contact info' | translate }}</b>
        <div v-html="contactInfo"></div>
      </template>
      <template v-if="directions">
        <i v-if="directions" v-html="directions"></i>
      </template>
    </div>
  </div>
</template>

<script>
  import translate from '../translate';
  import {round} from '../utils';

  export default {
    props: {
      banner: String,
      title: String,
      position: Array,
      authors: Array,
      address: String,
      contactInfo: String,
      directions: String,
      introduction: String
    },
    filters: {
      translate,
      round,
    }
  };
</script>

<style lang="scss">
  .memorial-card {
    .close {
      color: white;
      position: absolute;
      top: 10px;
      right: 10px;
      filter: drop-shadow(0 0 2px black);
    }
  }
</style>
