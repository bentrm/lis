<template>
  <div>
    <span v-if="loading">Loading...</span>
    <div v-if="memorial">
      <span @click="hide">
        <i class="fas fa-times-circle"></i>
      </span>
      <h3>{{memorial.title}}</h3>
      <img
        v-if="memorial.thumb"
        :src="memorial.thumb"
        :alt="memorial.title"
        class="Memorial-badge border border-primary rounded-circle align-self-center">
      <ul class="list-unstyled">
        <li v-for="author in memorial.authors" :key="author.id">
          <a :href="author.url">{{author.first_name}} {{author.last_name}}</a>
        </li>
      </ul>
      <div v-html="memorial.address"></div>
      <div v-html="memorial.contact_info"></div>
      <div v-html="memorial.directions"></div>
      <div v-html="memorial.introduction"></div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      api: Object,
      id: Number,
    },
    data() {
      return {
        error: null,
        loading: true,
        memorial: null
      };
    },
    created() {
      this.fetchData();
    },
    watch: {
      id: 'fetchData'
    },
    methods: {
      fetchData() {
        this.memorial = this.error = null;
        this.api
          .getMemorial(this.id)
          .then(json => {
            this.memorial = json;
            this.loading = false;
          });
      },
      hide () {
        this.$emit('hideMemorialDetail');
      }
    }
  };
</script>
