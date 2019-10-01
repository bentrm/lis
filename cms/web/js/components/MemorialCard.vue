<template>
  <div class="card memorial-card">
    <span class="close" v-on:click="$emit('hide')">
          <i class="fas fa-times"></i>
        </span>
    <img
      class="card-img-top"
      v-if="image"
      :src="image.banner"
      :alt="image.title">
    <div class="card-body">
      <h5>{{ title }}</h5>
      <ul class="list-unstyled">
        <li v-for="author in authors" :key="author.id">
          <a :href="author.url">{{author.first_name}} {{author.last_name}}</a>
        </li>
      </ul>
      <p>
        <b>{{ 'GPS Position' | translate}}: {{ position[0] | round }}, {{ position[1] | round }}</b>
      </p>
      <div v-if="introduction">
        <b>{{ 'Intro' | translate }}</b>
        <div v-html="introduction"></div>
      </div>
      <div v-if="address">
        <b>{{ 'Address' | translate }}</b>
        <address v-html="address"></address>
      </div>
      <div v-if="contactInfo">
        <b>{{ 'Contact info' | translate }}</b>
        <div v-html="contactInfo"></div>
      </div>
      <div v-if="directions">
        <b>{{ 'Directions' | translate }}</b>
        <i v-if="directions" v-html="directions"></i>
      </div>
      <div v-if="description">
        <b>{{ 'Description' | translate }}</b>
        <paragraph v-for="paragraph in description" :key="paragraph.id" v-bind="paragraph.value"></paragraph>
      </div>
    </div>
  </div>
</template>

<script>
  import Paragraph from './Paragraph.vue';
  import translate from '../translate';
  import {round} from '../utils';

  export default {
    props: {
      title: String,
      image: Object,
      position: Array,
      authors: Array,
      address: String,
      contactInfo: String,
      directions: String,
      introduction: String,
      description: Array,
    },
    components: {
      Paragraph,
    },
    filters: {
      translate,
      round,
    }
  };
</script>

<style lang="scss">
  @import '../../scss/variables';

  .memorial-card {
    .close {
      color: white;
      position: absolute;
      top: 10px;
      right: 10px;
      filter: drop-shadow(0 0 2px black);
    }

    .footnotes {
      font-size: $font-size-sm;

      ol {
        padding-left: 1.5rem;
      }
    }
  }
</style>
