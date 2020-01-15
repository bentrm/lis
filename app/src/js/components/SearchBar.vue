<template>
  <form class="form-inline d-flex search-bar" v-on:submit.prevent="onSubmit">
    <div class="flex-grow-1 ml-lg-4 mr-lg-2">
      <b-input-group>
        <label for="search-input" class="d-none">Suche</label>
        <b-form-input
          v-model="query"
          :placeholder="'Search' | translate"
          id="search-input"
          type="search"
          autocomplete="off"></b-form-input>
        <template v-slot:append>
          <b-dropdown
            ref="dropdown"
            class="search-dropdown"
            :text="'Search' | translate"
            variant="light"
            right
            :disabled="query.length < 3"
            :state="null"
          >
            <b-dropdown-header>{{ memorialsHeading }}</b-dropdown-header>
            <b-dropdown-item
              v-for="memorial in memorials"
              :key="memorial.id"
              :to="{name: 'memorial-detail', params: { mapStatePath: `@${memorial.position[0]},${memorial.position[1]},18z`, memorialId: memorial.id }}"
            >
              <div class="media">
                <cms-image
                  v-if="memorial.title_image"
                  :src="memorial.title_image.thumb"
                  :alt="memorial.title_image.title"
                  :title="memorial.title_image.title"
                  class="author-img border border-primary rounded-circle img-fluid mr-2 align-self-center"
                ></cms-image>
                <div class="media-body">
                  {{ memorial.name }}
                </div>
              </div>
            </b-dropdown-item>
            <b-dropdown-header>{{ authorsHeading }}</b-dropdown-header>
            <b-dropdown-item
              v-for="result in authors"
              :key="result.id"
              :to="{name: 'author-detail', params: { slug: result.slug, level: 'discover' }}"
              >
              <cms-image
                v-if="result.title_image"
                :src="result.title_image.thumb"
                :alt="result.title_image.title"
                :title="result.title_image.title"
                class="author-img border border-primary rounded-circle img-fluid mr-2 align-self-center"
              ></cms-image>
              {{ result.first_name }} {{ result.last_name }}
            </b-dropdown-item>
          </b-dropdown>
        </template>
      </b-input-group>
    </div>
  </form>
</template>

<script>
import CmsImage from './CmsImage.vue';
import api from '../Api';
import translate from '../translate';

export default {
  name: 'search-bar',
  components: {
    CmsImage,
  },
  filters: {
    translate
  },
  data: function() {
    return {
      limit: 5,
      query: '',
      authors: [],
      authorsCount: 0,
      memorials: [],
      memorialsCount: 0
    };
  },
  computed: {
    memorialsHeading() {
      return `${translate('Memorials')} (${this.memorials.length} / ${
        this.memorialsCount
      })`;
    },
    authorsHeading() {
      return `${translate('Authors')} (${this.authors.length} / ${
        this.authorsCount
      })`;
    }
  },
  methods: {
    onSubmit(e) {
      if (this.query.length > 2) {
        this.$refs.dropdown.show();
      }
    },

    resetResults() {
      const vm = this;

      vm.memorials = [];
      vm.memorialsCount = 0;
      vm.authors = [];
      vm.authorsCount = 0;
    },

    hideResults() {
      document.activeElement.blur();
    },

    fetchQueryResults: function(query) {
      const vm = this;
      const options = { search: query, limit: vm.limit };

      if (query.length < 3) {
        vm.resetResults();
        return;
      }

      api.getMemorials(options).then(json => {
        vm.memorials = json.results;
        vm.memorialsCount = json.count;
      });
      api.getAuthors(options).then(json => {
        vm.authors = json.results;
        vm.authorsCount = json.count;
      });
    }
  },
  watch: {
    query: function(newQuery, oldQuery) {
      const vm = this;
      if (newQuery.length < 3) {
        vm.resetResults();
      } else {
        vm.fetchQueryResults(newQuery);
      }
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';

.search-dropdown img {
  height: 1rem;
  width: 1rem;
}

.search-bar {
  position: relative;

  .search-bar-results {
    display: none;
    font-size: 0.8rem;
    position: absolute;
    left: 0;
    right: 0;
    background-color: white;
    border: $input-border-width solid $input-border-color;
    padding: $input-padding-x $input-padding-y;
    z-index: 1010;

    li {
      margin-bottom: 0.2rem;
    }
  }
}

.search-bar:focus-within {
  .search-bar-results {
    display: block;
  }
}
</style>
