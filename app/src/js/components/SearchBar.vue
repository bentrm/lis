<template>
  <form class="Search-bar form-inline d-flex" v-on:submit.prevent="onSubmit">
    <div class="flex-grow-1">
      <b-input-group>
        <label for="search-input" class="d-none">Suche</label>
        <b-form-input
          v-model="query"
          :placeholder="'Search term..' | translate"
          id="search-input"
          type="search"
          autocomplete="off"
        />
        <b-input-group-append>
          <b-button :disabled="query.length < 2" type="submit">{{ 'Search' | translate }}</b-button>
        </b-input-group-append>
      </b-input-group>
    </div>
  </form>
</template>

<script>
  import translate from '../translate';

  export default {

  filters: {
    translate
  },

  data() {
    return {
      query: '',
    };
  },

  methods: {
    onSubmit(e) {
      this.$emit('submit', this.query);
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';
</style>
