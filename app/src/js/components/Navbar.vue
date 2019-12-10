<template>
  <div class="MainNav">
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand :to="{name: 'index'}">
        <i class="fas fa-globe" data-fa-transform="shrink-10 up-2" data-fa-mask="fas fa-bookmark"></i>
        {{ 'Literary landscape' | translate }}
      </b-navbar-brand>

      <b-navbar-toggle target="header-menu">
        <i class="fas fa-bars"></i>
      </b-navbar-toggle>

      <b-collapse id="header-menu" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/map" active-class="active">{{ 'Map' | translate }}</b-nav-item>
          <b-nav-item :to="{name: 'author-list'}" active-class="active">{{ 'Authors' | translate }}</b-nav-item>
          <b-nav-item-dropdown :text="'More' | translate">
            <b-dropdown-item
              :to="{name: 'blog-page', params: { slug: 'about' }}"
            >{{ 'About' | translate }}</b-dropdown-item>
            <b-dropdown-item
              :to="{name: 'blog-page', params: { slug: 'imprint' }}"
            >{{ 'Imprint & data protection' | translate }}</b-dropdown-item>
            <b-dropdown-item :href="adminLink">{{ 'Admin' | translate }}</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item-dropdown :text="selectedLanguage.name">
            <button
              v-for="(name, code) in languages"
              name="language"
              :key="code"
              :value="code"
              type="button"
              class="dropdown-item"
              v-on:click="setLanguage(code)"
            >{{ name }}</button>
          </b-nav-item-dropdown>
        </b-navbar-nav>

        <search-bar class="flex-grow-1"></search-bar>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
  import {cmsHost} from '../config';
  import translate, {
    availableLanguages,
    getCurrentLanguage,
    setCurrentLanguage
  } from '../translate';
  import SearchBar from './SearchBar.vue';


  export default {
  components: { SearchBar },
  filters: { translate },

  computed: {
    languages() {
      return availableLanguages;
    },

    selectedLanguage() {
      let code = getCurrentLanguage();
      let name = availableLanguages[code];
      return { code, name };
    },

    adminLink() {
      return `${cmsHost}/cms/admin`;
    }
  },

  methods: {
    setLanguage(lang) {
      setCurrentLanguage(lang);
      this.$router.go();
    }
  }
};
</script>

<style lang="scss">
</style>
